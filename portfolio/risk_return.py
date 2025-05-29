def calc_portfolio_metrics(df, risk_free_rate=0.0):
    avg_daily_return = df['Portfolio_Return'].mean()
    std_dev = df['Portfolio_Return'].std()

    annualized_return = avg_daily_return * 252
    annualized_std = std_dev * (252 ** 0.5)
    sharpe_ratio = (annualized_return - risk_free_rate) / annualized_std if annualized_std != 0 else 0

    return {
        'avg_daily_return': avg_daily_return,
        'std_dev': std_dev,
        'sharpe_ratio': sharpe_ratio
    }