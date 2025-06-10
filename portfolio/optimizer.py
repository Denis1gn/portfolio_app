import numpy as np
from scipy.optimize import minimize

def optimize_portfolio_weights(mean_returns_daily, cov_matrix_daily,
                               target_volatility=0.20, init_guess=None):
    num_assets = len(mean_returns_daily)

    # Преобразуем в годовые значения
    mu = mean_returns_daily * 252
    sigma = cov_matrix_daily * 252

    # Целевая функция: максимизируем доходность → минимизируем отрицательную
    def neg_portfolio_return(weights):
        return -np.dot(weights, mu)

    # Ограничение на риск (годовая дисперсия ≤ целевой волатильности в квадрате)
    def risk_constraint(weights):
        return target_volatility**2 - np.dot(weights.T, np.dot(sigma, weights))

    constraints = [
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},        # сумма весов = 1
        {'type': 'ineq', 'fun': risk_constraint}               # риск ≤ целевого
    ]

    bounds = [(0, 1) for _ in range(num_assets)]  # без коротких продаж

    if init_guess is None:
        init_guess = np.array([1.0 / num_assets] * num_assets)

    result = minimize(
        neg_portfolio_return,
        init_guess,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )

    if not result.success:
        raise ValueError("Оптимизация не удалась, попробуй повысить уровень годовой волатильности")

    return result.x, -result.fun  # веса и ожидаемая доходность (годовая)
