import httpx
from mcp.server.fastmcp import FastMCP
from typing import TypedDict, List

from mla_mcp.conf import MLA_API_URL


# Initialize FastMCP server
mcp = FastMCP("ML Alpha")

class StockPriceResponse(TypedDict):
    labels: List[str]
    price: List[str]

@mcp.tool()
def get_stock_price(
    symbol: str,
    period: str = "annual",
    history: int = 10,
    resample: str = "MS"
) -> StockPriceResponse:
    """Retrieve historical stock prices for a given ticker symbol within a specified period.

    Args:
        symbol: The stock ticker symbol (e.g., AAPL, GOOGL)
        period: The period for which to retrieve stock prices (annual or quarterly)
        history: The number of years of historical data to retrieve
        resample: Pandas resample frequency (e.g., MS for month start)

    Returns:
        A dictionary containing:
            - labels: List of date labels for stock prices
            - price: List of stock prices corresponding to the date labels
    """
    response = httpx.get(
        f"{MLA_API_URL}/stock/prices/{symbol}",
        params={
            "period": period,
            "history": history,
            "resample": resample
        }
    )
    return response.json()
