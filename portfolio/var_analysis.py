import numpy as np
from scipy.stats import norm, binom

# Биномиальный тест на количество нарушений
def calculate_p_value(violations, n_observations, p=0.05):
    return 1 - binom.cdf(violations - 1, n_observations, p)

# Дельта-нормальный VaR
def delta_normal_var(returns, confidence_level=0.95):
    mean = np.mean(returns)
    std_dev = np.std(returns)
    var = norm.ppf(1 - confidence_level, mean, std_dev)
    return var

# Расчёт Value-at-Risk для портфеля
def perform_var_analysis(df, ma_window=50):
    df = df.copy()

    # Скользящие средние
    df['MA'] = df['Portfolio_Return'].rolling(window=ma_window).mean()
    df['EWMA'] = df['Portfolio_Return'].ewm(span=ma_window, adjust=False).mean()

    # VaR-модели
    df['Delta-Normal VaR'] = df['Portfolio_Return'].rolling(window=ma_window).apply(delta_normal_var)
    df['Var Historical'] = df['Portfolio_Return'].rolling(window=ma_window).apply(lambda x: np.percentile(x, 5))

    # Нарушения (violations)
    violations_ma = (df['Portfolio_Return'] < df['Delta-Normal VaR']).sum()
    violations_hist = (df['Portfolio_Return'] < df['Var Historical']).sum()
    n_observations = len(df)

    # P-значения
    p_value_ma = calculate_p_value(violations_ma, n_observations)
    p_value_hist = calculate_p_value(violations_hist, n_observations)

    # Дополнительные метрики
    df['Squared Returns'] = df['Portfolio_Return'] ** 2
    df['EWMA Variance'] = df['Squared Returns'].ewm(alpha=(1 - 0.94)).mean()
    df['EWMA Volatility'] = np.sqrt(df['EWMA Variance'])
    df['r/σ_EWMA'] = df['Portfolio_Return'] / df['EWMA Volatility']

    results = {
        'Violations, Delta-Normal VaR': violations_ma,
        'Violations, Historical VaR': violations_hist,
        'Observations': n_observations,
        'Expected Violations (5%)': n_observations * 0.05,
        'p-value, Delta-Normal VaR': p_value_ma,
        'p-value, Historical VaR': p_value_hist
    }

    return df, results, ma_window