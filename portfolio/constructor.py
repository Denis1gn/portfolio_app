import pandas as pd

def build_portfolio_df(dfs, tickers, weights):
    merged = pd.concat(dfs, axis=1)
    price_cols = [f'{t}_Stock_Price' for t in tickers]
    ret_cols = [f'{t}_Daily_Return' for t in tickers]

    merged['Portfolio_Price'] = sum(weights[i] * merged[price_cols[i]] for i in range(len(weights)))
    merged['Portfolio_Return'] = sum(weights[i] * merged[ret_cols[i]] for i in range(len(weights)))
    
    return merged