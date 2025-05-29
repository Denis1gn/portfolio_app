import numpy as np
from scipy.optimize import minimize

def optimize_portfolio_weights(mean_returns_daily, cov_matrix_daily, rf=0.0, init_guess=None):
    num_assets = len(mean_returns_daily)

    # Преобразуем в годовые значения
    mean_returns_annual = mean_returns_daily * 252
    cov_matrix_annual = cov_matrix_daily * 252

    def negative_sharpe_ratio(weights):
        port_return = np.dot(weights, mean_returns_annual)
        port_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix_annual, weights)))
        if port_vol == 0:
            return np.inf
        return -(port_return - rf) / port_vol

    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))

    if init_guess is None:
        init_guess = np.array([1. / num_assets] * num_assets)

    history = []

    def callback(xk):
        sharpe = -negative_sharpe_ratio(xk)
        history.append(sharpe)

    result = minimize(negative_sharpe_ratio, init_guess,
                      method='SLSQP', bounds=bounds,
                      constraints=constraints, callback=callback)

    if not result.success:
        raise ValueError("❌ Не удалось провести оптимизацию портфеля")

    return result.x, -result.fun, history