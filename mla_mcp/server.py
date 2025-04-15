import httpx
from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, TypedDict
from pydantic import BaseModel

from mla_mcp.conf import MLA_API_URL

# Initialize FastMCP server
mcp = FastMCP("ML Alpha")

class StockPriceResponse(BaseModel):
    labels: List[str]
    price: List[str]

class CompanySummary(BaseModel):
    companyName: str
    description: str
    industry: str
    sector: str
    symbol: str

class ETFSummary(BaseModel):
    name: str
    symbol: str
    description: str
    countriesAllocation: Dict[str, float]
    sectors: Dict[str, float]

class ExchangeRecommendation(BaseModel):
    list_top_recommendations: List[Dict[str, Any]]
    ticker_action: str
    ticker_rank: float

class FinancialScore(BaseModel):
    date: str
    dividendScore: float
    longTermValueScore: float
    mediumTermValueScore: float
    overallScore: float
    safetyScore: float
    shortTermValueScore: float

class StocksListResponse(BaseModel):
    companies: Dict[str, str]
    etfs: List[Dict[str, str]]

class ScreenerRequest(BaseModel):
    filters: List[Dict[str, Any]]
    industries: List[str]
    marketcaps: List[str]
    sectors: List[str]
    page: int
    perPage: int
    sortBy: List[Dict[str, str]]

class TopFinancialScoresRequest(BaseModel):
    industries: List[str]
    marketcaps: List[str]
    sectors: List[str]
    limit: int
    min_price: float
    sortby: str
    weights: List[str]


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

@mcp.tool()
def get_exchange_recommendation(symbol: str, weights: Dict[str, float]) -> ExchangeRecommendation:
    """Get stock exchange recommendation based on provided weights.

    Args:
        symbol: The stock ticker symbol
        weights: Weighted scores for recommendation criteria (e.g., {"criteria1": 0.5})

    Returns:
        Exchange recommendation including top recommendations and ticker action
    """
    response = httpx.post(
        f"{MLA_API_URL}/stock/exchange_recommendation/{symbol}",
        json={"weights": weights}
    )
    return response.json()

@mcp.tool()
def get_financial_check(symbol: str) -> Dict:
    """Get financial checks for a stock.

    Args:
        symbol: The stock ticker symbol

    Returns:
        Comprehensive financial check data including various scores and metrics
    """
    response = httpx.get(f"{MLA_API_URL}/stock/financial_check/{symbol}")
    return response.json()

@mcp.tool()
def get_financial_data(
    symbol: str,
    period: str = "annual",
    history: int = 10,
    categories: List[str] = None
) -> Dict:
    """Get financial data for a stock including revenue, profit, and growth metrics.

    Args:
        symbol: The stock ticker symbol
        period: The period for data (annual or quarterly)
        history: Number of years of historical data
        categories: List of specific financial categories to retrieve

    Returns:
        Historical financial data including dates, revenue, profits and related metrics
    """
    params = {
        "period": period,
        "history": history
    }
    if categories:
        if 'date' not in categories:
            categories.append('date')

        params["categories"] = ','.join(categories)

    response = httpx.get(
        f"{MLA_API_URL}/stock/financial_data/{symbol}",
        params=params
    )
    return response.json()

@mcp.tool()
def get_financial_data_ttm(symbol: str) -> Dict:
    """Get TTM (Trailing Twelve Months) financial data for a stock.

    Args:
        symbol: The stock ticker symbol

    Returns:
        TTM financial data
    """
    response = httpx.get(f"{MLA_API_URL}/stock/financial_data_ttm/{symbol}")
    return response.json()

@mcp.tool()
def get_financial_score(symbol: str) -> List[FinancialScore]:
    """Get the financial score for a stock.

    Args:
        symbol: The stock ticker symbol

    Returns:
        List of financial scores including various component scores
    """
    response = httpx.get(f"{MLA_API_URL}/stock/financial_score/{symbol}")
    return response.json()

@mcp.tool()
def get_all_stocks() -> StocksListResponse:
    """Returns a list of all stock tickers along with their company names and ETF information.

    Returns:
        Dictionary containing companies and ETFs information
    """
    response = httpx.get(f"{MLA_API_URL}/stocks/all")
    return response.json()

@mcp.tool()
def get_exchange_recommendation_list(symbols: str, weights: Dict[str, float]) -> Dict[str, Any]:
    """Get stock exchange recommendations for multiple tickers based on provided weights.

    Args:
        symbols: Comma-separated list of stock ticker symbols (e.g., "AAPL,MSFT")
        weights: Weighted scores for recommendation criteria

    Returns:
        Exchange recommendations for the specified tickers
    """
    response = httpx.post(
        f"{MLA_API_URL}/stocks/exchange_recommendation_list/{symbols}",
        json={"weights": weights}
    )
    return response.json()

@mcp.tool()
def get_correlations(tickers: str, period: int = 90) -> Dict[str, Any]:
    """Get correlations for a list of stock tickers over a specified period.

    Args:
        tickers: Comma-separated list of stock tickers
        period: Number of days to look back (10-365)

    Returns:
        Dictionary with stock correlations
    """
    response = httpx.get(
        f"{MLA_API_URL}/stocks/get-correlations",
        params={"tickers": tickers, "period": period}
    )
    return response.json()

@mcp.tool()
def get_last_prices(ticker_list: str) -> Dict[str, float]:
    """Get the last prices for a list of tickers.

    Args:
        ticker_list: Comma-separated list of ticker symbols (e.g., "AAPL,MSFT")

    Returns:
        Dictionary mapping ticker symbols to their last prices
    """
    response = httpx.get(f"{MLA_API_URL}/stocks/get-last-prices/{ticker_list}")
    return response.json()

@mcp.tool()
def get_scores(ticker_list: str) -> Dict[str, List]:
    """Get scores for a list of tickers.

    Args:
        ticker_list: Comma-separated list of ticker symbols

    Returns:
        Dictionary containing arrays of scores and related data
    """
    response = httpx.get(f"{MLA_API_URL}/stocks/get-scores/{ticker_list}")
    return response.json()

@mcp.tool()
def get_stocks_info(tickers: List[str]) -> Dict:
    """Get stocks information for a list of tickers.

    Args:
        tickers: List of ticker symbols

    Returns:
        Dictionary containing stock information
    """
    response = httpx.post(f"{MLA_API_URL}/stocks/info", json={"tickers": tickers})
    return response.json()

@mcp.tool()
def get_latest_filings(limit: int = None) -> Dict[str, List]:
    """Returns the latest filings data for companies.

    Args:
        limit: Optional maximum number of results to retrieve

    Returns:
        Dictionary containing arrays of filing data
    """
    params = {"limit": limit} if limit else None
    response = httpx.get(f"{MLA_API_URL}/stocks/latest-fillings", params=params)
    return response.json()

@mcp.tool()
def get_screener(filters: ScreenerRequest) -> Dict[str, Any]:
    """Perform a stock screener query based on specified filters.

    Args:
        filters: Dictionary containing filter criteria, pagination, and sorting options

    Returns:
        Dictionary containing screener results and metadata
    """
    response = httpx.post(f"{MLA_API_URL}/stocks/screener", json=filters)
    return response.json()

@mcp.tool()
def get_top_financial_scores(filters: TopFinancialScoresRequest) -> List[Dict[str, Any]]:
    """Get a list of stocks with top financial scores.

    Args:
        filters: Dictionary containing filter criteria and sorting options

    Returns:
        List of stocks with their financial scores
    """
    response = httpx.post(f"{MLA_API_URL}/stocks/top_financial_scores", json=filters)
    return response.json()
