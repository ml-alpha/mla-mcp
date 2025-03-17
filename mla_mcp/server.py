import httpx
from mcp.server.fastmcp import FastMCP
from typing import Any

from mla_mcp.conf import MLA_API_URL


# Initialize FastMCP server
mcp = FastMCP("ML Alpha")


@mcp.tool()
def get_stock_price(symbol: str) -> Any:
    """Get the stock price

    Args:
        symbol: The ticker of the stock like AAPL, GOOGL, etc.
    """
    response = httpx.get(
        f"{MLA_API_URL}/stock/prices/{symbol}?period=annual&history=10&resample=MS"
    )
    return response.json()
