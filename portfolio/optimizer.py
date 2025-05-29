# --- optimizer.py ---
import numpy as np
from scipy.optimize import minimize

def optimize_portfolio_weights(mean_returns, cov_matrix, init_guess=None):
    num_assets = len(mean_returns)

    def portfolio_volatility(weights):
        return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))

    # Если не задано начальное приближение — берём равные веса
    if init_guess is None:
        init_guess = np.array([1. / num_assets] * num_assets)

    history = []

    def callback(xk):
        vol = portfolio_volatility(xk)
        history.append(vol)

    result = minimize(portfolio_volatility, init_guess,
                      method='SLSQP', bounds=bounds,
                      constraints=constraints, callback=callback)

    if not result.success:
        raise ValueError("❌ Не удалось провести оптимизацию портфеля")

    return result.x, result.fun, history