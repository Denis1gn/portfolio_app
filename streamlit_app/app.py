import streamlit as st
import datetime as dt
from ui import (
    get_user_inputs, get_weights_ui, plot_portfolio_return, display_metrics,
    plot_return_distribution, display_asset_statistics, plot_correlation_heatmap,
    plot_volatility_function, plot_var_analysis, display_var_results
)
from loaders.moex_loader import get_moex_data_and_prepare
from loaders.risk_free_rate import get_risk_free_rate
from portfolio.constructor import build_portfolio_df
from portfolio.risk_return import calc_portfolio_metrics
from portfolio.optimizer import optimize_portfolio_weights
from portfolio.var_analysis import perform_var_analysis

import numpy as np
import copy

def fetch_data(tickers, start_date, end_date):
    dfs = []
    for t in tickers:
        df = get_moex_data_and_prepare(t, start_date, end_date)
        if not df.empty:
            dfs.append(df)
        else:
            st.warning(f"Нет данных для {t}")
    return dfs

def main():
    st.set_page_config(layout="wide", page_title="Анализ портфеля")
    st.title("📊 Анализ инвестиционного портфеля на MOEX")

    tickers, start_date, end_date = get_user_inputs()
    if not tickers:
        st.info("Выберите хотя бы один тикер")
        return

    if 'weights' not in st.session_state or len(st.session_state.weights) != len(tickers):
        st.session_state.weights = [1.0 / len(tickers)] * len(tickers)

    weights = get_weights_ui(tickers, st.session_state.weights)
    st.session_state.weights = weights

    if abs(sum(weights) - 1.0) > 0.01:
        st.error("Сумма весов должна быть 1.0")
        return

    if st.button("📥 Загрузить и проанализировать") or 'port_df' in st.session_state:
        if 'dfs' not in st.session_state:
            st.session_state.dfs = fetch_data(tickers, start_date, end_date)

        if st.session_state.dfs:
            st.session_state.port_df = build_portfolio_df(st.session_state.dfs, tickers, weights)
            st.session_state.rf = get_risk_free_rate(start_date.strftime("%Y-%m-%d")) or 0.0
            st.session_state.metrics = calc_portfolio_metrics(st.session_state.port_df, st.session_state.rf)
            st.session_state.metrics['cumulative_return'] = (1 + st.session_state.port_df['Portfolio_Return']).prod() - 1
            st.session_state.tickers = tickers
            st.session_state.weights = weights

    if 'port_df' in st.session_state:
        plot_portfolio_return(st.session_state.port_df, key_suffix="fact")
        plot_return_distribution(st.session_state.port_df, key="fact")
        display_metrics(st.session_state.metrics)
        display_asset_statistics(st.session_state.port_df, st.session_state.tickers, st.session_state.rf)
        plot_correlation_heatmap(st.session_state.port_df)

        # Расчет и отображение VaR 
        var_data, var_results, ma_window = perform_var_analysis(st.session_state.port_df)
        plot_var_analysis(var_data, ma_window)
        display_var_results(var_data, var_results, ma_window)

        if st.button("🚀 Оптимизировать портфель"):
            mean_returns = st.session_state.port_df[[f"{t}_Daily_Return" for t in st.session_state.tickers]].mean()
            cov_matrix = st.session_state.port_df[[f"{t}_Daily_Return" for t in st.session_state.tickers]].cov()
            init_guess = copy.deepcopy(st.session_state.weights)

            opt_weights, min_vol, history = optimize_portfolio_weights(
                mean_returns.values, cov_matrix.values, init_guess
            )

            st.session_state.opt_weights = opt_weights
            st.session_state.history = history
            st.session_state.opt_port_df = build_portfolio_df(st.session_state.dfs, st.session_state.tickers, opt_weights)
            st.session_state.opt_metrics = calc_portfolio_metrics(st.session_state.opt_port_df, st.session_state.rf)
            st.session_state.opt_metrics['cumulative_return'] = (1 + st.session_state.opt_port_df['Portfolio_Return']).prod() - 1

    if 'opt_port_df' in st.session_state:
        st.subheader("🎯 Оптимальные веса")
        for t, w in zip(st.session_state.tickers, st.session_state.opt_weights):
            st.write(f"{t}: {w:.2%}")

        plot_portfolio_return(st.session_state.opt_port_df, key_suffix="opt")
        display_metrics(st.session_state.opt_metrics)
        plot_volatility_function(st.session_state.history)

if __name__ == "__main__":
    main()