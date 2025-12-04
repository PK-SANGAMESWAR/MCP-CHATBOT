import asyncio
import re
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import ToolMessage, SystemMessage
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

# ----------------------------------------
# MCP SERVERS
# ----------------------------------------
SERVERS = {
    "math": {
        "transport": "stdio",
        "command": "C:\\Python310\\Scripts\\uv.exe",
        "args": ["run", "fastmcp", "run", "C:\\Users\\LOQ\\Downloads\\MCP_MATH_SERVER\\main.py"]
    },
    "expense": {
        "transport": "streamable_http",
        "url": "https://considerable-lime-toad.fastmcp.app/mcp"
    },
    "manim-server": {
        "transport": "stdio",
        "command": "C:\\Python310\\python.exe",
        "args": ["C:\\Users\\LOQ\\Downloads\\manim-mcp-server\\src\\manim_server.py"],
        "env": {"MANIM_EXECUTABLE": "C:\\Python310\\Scripts\\manim.exe"}
    }
}

# ----------------------------------------
# MATH QUESTION DETECTOR
# ----------------------------------------
def is_math_question(text: str) -> bool:
    math_keywords = [
        "add", "plus", "+", "sum",
        "subtract", "minus", "-", "difference",
        "multiply", "times", "*", "product",
        "divide", "/", "quotient"
    ]
    if any(k in text.lower() for k in math_keywords):
        return True

    if re.search(r"\b\d+(\.\d+)?\s*[\+\-\*/]\s*\d+(\.\d+)?\b", text):
        return True

    return False


# ----------------------------------------
# MAIN AGENT FUNCTION
# ----------------------------------------
async def run_agent(prompt: str):

    # Connect to all MCP servers
    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()
    named_tools = {tool.name: tool for tool in tools}

    # Initialize LLM
    llm = ChatOllama(model="llama3.2:3b", base_url="http://localhost:11434")
    llm_with_tools = llm.bind_tools(tools)

    # System instructions
    system_rule = SystemMessage(
        content=(
            "USE TOOLS ONLY WHEN NECESSARY:\n"
            "- Math tool → ONLY for clear arithmetic.\n"
            "- Expense tool → ONLY for expense-related tasks.\n"
            "- Manim tool → ONLY for animation generation.\n"
            "- Otherwise answer directly without tools."
        )
    )

    # ---------- STEP 1: direct LLM for non-math ----------
    if not is_math_question(prompt):
        response = await llm.ainvoke(prompt)
        return response.content

    # ---------- STEP 2: let LLM pick a tool ----------
    response = await llm_with_tools.ainvoke([system_rule, prompt])

    # No tool selected
    if not getattr(response, "tool_calls", None):
        return response.content

    # ---------- STEP 3: Execute all tool calls ----------
    tool_messages = []

    for tc in response.tool_calls:
        tool_name = tc["name"]
        tool_args = tc["args"]
        tool_call_id = tc["id"]

        try:
            tool_result = await named_tools[tool_name].ainvoke(tool_args)
        except Exception as e:
            tool_result = f"Tool Error: {e}"

        tool_messages.append(
            ToolMessage(
                content=str(tool_result),
                tool_name=tool_name,
                tool_call_id=tool_call_id
            )
        )

    # ---------- STEP 4: Final LLM answer ----------
    final = await llm_with_tools.ainvoke([response] + tool_messages)
    return final.content
