import pandas as pd

def build_portfolio_df(dfs, tickers, weights):
    from functools import reduce
    import pandas as pd

    if len(dfs) != len(tickers):
        raise ValueError("Количество DataFrame и тикеров не совпадает")

    merged = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True, how='outer'), dfs)
    merged = merged.sort_index().dropna()

    # Столбцы цен и доходностей
    price_cols = [f"{t}_Stock_Price" for t in tickers if f"{t}_Stock_Price" in merged.columns]
    return_cols = [f"{t}_Daily_Return" for t in tickers if f"{t}_Daily_Return" in merged.columns]

    if len(price_cols) != len(weights) or len(return_cols) != len(weights):
        missing = [t for i, t in enumerate(tickers) if f"{t}_Stock_Price" not in merged.columns or f"{t}_Daily_Return" not in merged.columns]
        raise KeyError(f"Некорректные данные для тикеров: {missing}")

    merged['Portfolio_Price'] = sum(weights[i] * merged[price_cols[i]] for i in range(len(weights)))
    merged['Portfolio_Return'] = sum(weights[i] * merged[return_cols[i]] for i in range(len(weights)))

    return merged