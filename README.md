# MCP Server For ML Alpha

ML Alpha MCP is a server implementation that provides a comprehensive API for accessing financial market data, stock analysis, and investment insights.

## Features

- Historical stock price data retrieval
- Company and ETF summaries
- Financial analysis and scoring
- Stock screening capabilities
- SEC filing data access
- Competitor analysis
- Exchange recommendations

## API Reference

The server provides the following main categories of tools:

### Price Data
- `get_stock_price`: Retrieve historical stock prices
- `get_last_prices`: Get latest prices for multiple stocks

### Company Information
- `get_company_summary`: Get company overview
- `get_etf_summary`: Get ETF details
- `get_competitors`: Find company competitors

### Financial Analysis
- `get_financial_check`: Complete financial health check
- `get_financial_data`: Historical financial metrics
- `get_financial_score`: Comprehensive scoring
- `get_financial_data_ttm`: TTM financial data

### Market Analysis
- `get_correlations`: Stock price correlations
- `get_exchange_recommendation`: Trading recommendations
- `get_screener`: Advanced stock screening
- `get_top_financial_scores`: Top performing stocks

### Documentation
- `get_10k_sections`: Access SEC filing sections
- `get_latest_filings`: Recent SEC filings


## Connect to the MCP server:

```
{
    "mcpServers": {
        "mcp-mlalpha":{
            "command": "uvx",
            "args": [
            "--python=3.12",
            "--from",
            "git+https://github.com/ml-alpha/mla-mcp",
            "mcp-mlalpha"
            ]
        }
    }
}
```
