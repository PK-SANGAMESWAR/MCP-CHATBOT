import asyncio
import re
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import ToolMessage, SystemMessage
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------------
# DEFINE MCP SERVERS
# --------------------------------------------------------
SERVERS = {
    "math": {
        "transport": "stdio",
        "command": "C:\\Python310\\Scripts\\uv.exe",
        "args": [
            "run",
            "fastmcp",
            "run",
            "C:\\Users\\LOQ\\Downloads\\MCP_MATH_SERVER\\main.py"
        ]
    },
    "expense": {
        "transport": "streamable_http",
        "url": "https://considerable-lime-toad.fastmcp.app/mcp"
    },
    "manim-server": {
        "transport": "stdio",
        "command": "C:\\Python310\\python.exe",
        "args": [
            "C:\\Users\\LOQ\\Downloads\\manim-mcp-server\\src\\manim_server.py"
        ],
        "env": {
            "MANIM_EXECUTABLE": "C:\\Python310\\Scripts\\manim.exe"
        }
    }
}

# --------------------------------------------------------
# MATH DETECTOR
# --------------------------------------------------------
def is_math_question(text: str) -> bool:
    math_keywords = ["add", "plus", "+", "sum",
                     "subtract", "minus", "-", "difference",
                     "multiply", "times", "*", "product",
                     "divide", "/", "quotient"]

    if any(k in text.lower() for k in math_keywords):
        return True

    if re.search(r"\b\d+(\.\d+)?\s*[\+\-\*/]\s*\d+(\.\d+)?\b", text):
        return True

    return False


async def main():

    # --------------------------------------------------------
    # CONNECT TO MCP SERVERS
    # --------------------------------------------------------
    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()
    named_tools = {tool.name: tool for tool in tools}

    # --------------------------------------------------------
    # INITIALIZE OLLAMA
    # --------------------------------------------------------
    llm = ChatOllama(
        model="llama3.2:3b",
        base_url="http://localhost:11434"
    )
    llm_with_tools = llm.bind_tools(tools)

    # --------------------------------------------------------
    # SYSTEM RULES FOR TOOL USAGE
    # --------------------------------------------------------
    system_rule = SystemMessage(
        content=(
            "TOOL USAGE RULES:\n"
            "- Use the math tool ONLY for arithmetic involving numbers.\n"
            "- Use the expense tool ONLY for expense queries.\n"
            "- Use the manim tool ONLY for generating mathematics animations.\n"
            "- For general questions, answer directly.\n"
        )
    )

    # --------------------------------------------------------
    # USER QUESTION
    # --------------------------------------------------------
    prompt = "What is the capital of India?"

    # --------------------------------------------------------
    # STEP 1 — If not math, bypass tools
    # --------------------------------------------------------
    if not is_math_question(prompt):
        print("\n🔍 Non-math question → Answering without tools.")
        direct_response = await llm.ainvoke(prompt)
        print("\nLLM Reply:", direct_response.content)
        return

    # --------------------------------------------------------
    # STEP 2 — ALLOW TOOL CALLS FOR MATH ONLY
    # --------------------------------------------------------
    response = await llm_with_tools.ainvoke([system_rule, prompt])

    if not getattr(response, "tool_calls", None):
        print("\nLLM Reply:", response.content)
        return

    # --------------------------------------------------------
    # STEP 3 — PROCESS ALL TOOL CALLS
    # --------------------------------------------------------
    tool_messages = []

    for tc in response.tool_calls:
        selected_tool = tc["name"]
        selected_args = tc["args"]
        tool_call_id = tc["id"]

        print("\nSelected tool:", selected_tool)
        print("Arguments:", selected_args)

        # Execute tool
        tool_result = await named_tools[selected_tool].ainvoke(selected_args)

        # Append formatted tool message
        tool_messages.append(
            ToolMessage(
                content=str(tool_result),
                tool_name=selected_tool,
                tool_call_id=tool_call_id
            )
        )

    # --------------------------------------------------------
    # STEP 4 — FINAL LLM RESPONSE AFTER TOOL OUTPUT
    # --------------------------------------------------------
    final_response = await llm_with_tools.ainvoke([response] + tool_messages)

    print("\nFinal Response:\n", final_response.content)


if __name__ == "__main__":
    asyncio.run(main())
