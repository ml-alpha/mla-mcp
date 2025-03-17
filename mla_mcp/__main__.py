from mla_mcp.server import mcp

def main():
    print("Starting FastMCP server...")
    mcp.run(transport='sse')


if __name__ == "__main__":
    main()