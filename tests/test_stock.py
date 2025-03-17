import mla_mcp.server as srv
from typing import Dict

def test_get_stock_price():
    resp = srv.get_stock_price("AAPL")
    print(resp)
    
    resp = srv.StockPriceResponse(**resp)
    assert len(resp.labels) > 0

def test_get_company_summary():
    resp = srv.get_company_summary("AAPL")
    print(resp)
    
    resp = srv.CompanySummary(**resp)
    assert resp.symbol == "AAPL"
    assert resp.companyName != ""

def test_get_etf_summary():
    resp = srv.get_etf_summary("SPY")
    print(resp)
    
    resp = srv.ETFSummary(**resp)
    assert resp.symbol == "SPY"
    assert len(resp.sectors) > 0

def test_get_competitors():
    resp = srv.get_competitors("AAPL")
    print(resp)
    
    assert isinstance(resp, list)
    assert len(resp) > 0

def test_get_10k_sections():
    sections = ["Item 1", "Item 7"]
    resp = srv.get_10k_sections("AAPL", sections)
    print(resp)
    
    assert isinstance(resp, list)
    assert len(resp) > 0

def test_get_exchange_recommendation():
    weights: Dict[str, float] = {'shortTermValueScore': 1, 'mediumTermValueScore': 5, 'longTermValueScore': 2,
            'safetyScore': 2, 'dividendScore': 3}
    resp = srv.get_exchange_recommendation("AAPL", weights)
    print(resp)
    
    resp = srv.ExchangeRecommendation(**resp)
    assert isinstance(resp.ticker_rank, float)

def test_get_financial_check():
    resp = srv.get_financial_check("AAPL")
    print(resp)

    assert isinstance(resp['fnd_totalAssets'], float)

def test_get_financial_data():
    resp = srv.get_financial_data("AAPL", categories=['date', 'fnd_revenue'])
    print(resp)
    
    assert len(resp['date']) > 0

def test_get_financial_data_ttm():
    resp = srv.get_financial_data_ttm("AAPL")
    print(resp)
    
    assert isinstance(resp, dict)

def test_get_financial_score():
    resp = srv.get_financial_score("AAPL")
    print(resp)
    
    assert len(resp) > 0
    resp_item = srv.FinancialScore(**resp[0])
    assert isinstance(resp_item.overallScore, float)

# def test_get_all_stocks():
#     resp = srv.get_all_stocks()
#     print(resp)
    
#     resp = srv.StocksListResponse(**resp)
#     assert len(resp.companies) > 0
#     assert isinstance(resp.etfs, list)

def test_get_exchange_recommendation_list():
    weights = {'shortTermValueScore': 1, 'mediumTermValueScore': 5, 'longTermValueScore': 2,
            'safetyScore': 2, 'dividendScore': 3}
    resp = srv.get_exchange_recommendation_list("AAPL,MSFT", weights)
    print(resp)
    
    assert isinstance(resp, dict)

def test_get_correlations():
    resp = srv.get_correlations("AAPL,MSFT", period=90)
    print(resp)
    
    assert isinstance(resp, dict)

def test_get_last_prices():
    resp = srv.get_last_prices("AAPL,MSFT")
    print(resp)
    
    assert isinstance(resp, dict)
    assert all(isinstance(v, float) for v in resp.values())

def test_get_scores():
    resp = srv.get_scores("AAPL,MSFT")
    print(resp)
    
    assert isinstance(resp, dict)

def test_get_stocks_info():
    resp = srv.get_stocks_info(["AAPL", "MSFT"])
    print(resp)
    
    assert isinstance(resp, dict)

def test_get_latest_filings():
    resp = srv.get_latest_filings(limit=10)
    print(resp)
    
    assert isinstance(resp, dict)

def test_get_screener():
    filters = {"filters": [{"cat": "fnd_revenue", "op": ">=", "val": 1e10}]}
    resp = srv.get_screener(filters)
    print(resp)
    
    assert isinstance(resp, dict)

def test_get_top_financial_scores():
    data = {
        "sortby": "overallScore",
        "limit": 100,
        "sectors": ["Technology", "Healthcare", "Utilities"],
        "industries": ["Semiconductors", "Aluminum"],
        "marketcaps":  ["large", "medium", "small"],
        "weights": {
            "shortTermValueScore": 0.5,
            "mediumTermValueScore": 0.5,
            "longTermValueScore": 0.5,
            "dividendScore": 0.5,
            "safetyScore": 0.5,
        }
    }
    resp = srv.get_top_financial_scores(data)
    print(resp)
    
    assert isinstance(resp, list)

