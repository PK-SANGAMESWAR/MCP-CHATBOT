from fastmcp import FastMCP

##create a proxy to your FastMCP server
##FastMCP Cloud uses streamable HTTP 

mcp = FastMCP.as_proxy(
    "https://considerable-lime-toad.fastmcp.app/mcp",
    name = "SANGAMESWAR"
)

if __name__ == "__main__":
    mcp.run()