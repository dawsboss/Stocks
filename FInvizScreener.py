import analysis_engine.finviz.fetch_api as fv

url = (
    'https://finviz.com/screener.ashx?'
    'v=111&'
    'f=cap_midunder,exch_nyse,fa_div_o5,idx_sp500'
    '&ft=4')
res = fv.fetch_tickers_from_screener(url=url)
print(res)


