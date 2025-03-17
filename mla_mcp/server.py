import httpx
from mcp.server.fastmcp import FastMCP
from typing import TypedDict, List, Dict

from mla_mcp.conf import MLA_API_URL


# Initialize FastMCP server
mcp = FastMCP("ML Alpha")

class StockPriceResponse(TypedDict):
    labels: List[str]
    price: List[str]

class CompanySummary(TypedDict):
    companyName: str
    description: str
    industry: str
    sector: str
    symbol: str

class ETFSummary(TypedDict):
    name: str
    symbol: str
    description: str
    countriesAllocation: Dict[str, float]
    sectors: Dict[str, float]

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

@mcp.tool()
def get_company_summary(symbol: str) -> CompanySummary:
    """Retrieves summary information about a company by its stock ticker symbol.

    Args:
        symbol: The stock ticker symbol of the company

    Returns:
        Company summary information including name, description, industry, and sector
    """
    response = httpx.get(f"{MLA_API_URL}/stock/company-summary/{symbol}")
    return response.json()

@mcp.tool()
def get_etf_summary(symbol: str) -> ETFSummary:
    """Get detailed summary information about an ETF by its ticker symbol.

    Args:
        symbol: The ticker symbol of the ETF (e.g., VTI)

    Returns:
        ETF summary including name, description, country and sector allocations
    """
    response = httpx.get(f"{MLA_API_URL}/stock/etf-summary/{symbol}")
    return response.json()

@mcp.tool()
def get_competitors(symbol: str) -> List[str]:
    """Retrieve a list of competitor tickers for a specified company ticker.

    Args:
        symbol: The stock ticker symbol for which to retrieve competitors

    Returns:
        List of competitor ticker symbols
    """
    response = httpx.get(f"{MLA_API_URL}/stock/competitors/{symbol}")
    return response.json()

@mcp.tool()
def get_10k_sections(symbol: str, sections: List[str]) -> List[str]:
    """Fetch specific sections from the 10-K filing for a given stock ticker.

    Args:
        symbol: Stock ticker symbol
        sections: List of 10-K sections to retrieve (e.g., ["Item 1", "Item 7"])

    Returns:
        List of section contents as strings
    """
    response = httpx.post(
        f"{MLA_API_URL}/stock/10k-sections/{symbol}",
        json={"sections": sections}
    )
    return response.json()
