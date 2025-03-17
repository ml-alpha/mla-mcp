from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP


MLA_API_BASE_URL = "https://api.mlalpha.com"
MLA_API_VERSION = "v0.1"
MLA_API_URL = f"{MLA_API_BASE_URL}/{MLA_API_VERSION}"

# Initialize FastMCP server
mcp = FastMCP("weather")

@mcp.tool()
def get_stock_price(symbol: str) -> Any:
    """Get the stock price

    Args:
        symbol: The ticker of the stock like AAPL, GOOGL, etc.
    """
    response = httpx.get(f"{MLA_API_URL}/stock/prices/{symbol}?period=annual&history=10&resample=MS")
    return response.json()


def main():
    print("Starting FastMCP server...")
    mcp.run(transport='sse')

if __name__ == "__main__":
    main()