from mla_mcp.server import mcp


def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()