import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np


def get_user_inputs():
    from datetime import date, timedelta

    TICKER_OPTIONS = [
        'SBER', 'GAZP', 'LKOH', 'TATN', 'ROSN', 'VTBR', 'NVTK', 'GMKN', 'CHMF',
        'NLMK', 'PLZL', 'PHOR', 'MGNT', 'MTSS', 'MOEX', 'HYDR', 'FEES', 'IRAO', 'AFLT',
        'ALRS', 'AFKS', 'MVID', 'PIKK', 'OZON', 'FIXP', 'SGZH', 'SNGS', 'SNGSP', 'TATNP',
        'SBERP', 'TRNFP', 'RUAL', 'AKRN', 'MAGN', 'RTKM', 'RTKMP', 'POLY', 'TRMK', 'UPRO',
        'URKA', 'UWGN', 'ENPG', 'SVCB', 'LSNGP', 'LSNG', 'RASP', 'MSNG', 'NMTP', 'CBOM',
        'DSKY', 'LNTA', 'MFON', 'AGRO', 'BANE', 'BANEP', 'DIXY', 'EONR', 'LSRG', 'MRKH',
        'MSRS', 'MSTT', 'MTLR', 'MTLRP', 'OGKB', 'PHST', 'RSTI', 'SVAV', 'VSMO', 'VZRZ', 'YDEX'
    ]

    tickers = st.multiselect("Выберите тикеры", TICKER_OPTIONS, default=['SBER', 'GAZP'])
    start = st.date_input("Дата начала", date.today() - timedelta(days=365))
    end = st.date_input("Дата конца", date.today())
    return tickers, start, end


def get_weights_ui(tickers, saved_weights=None):
    weights = []
    cols = st.columns(len(tickers))
    for i, t in enumerate(tickers):
        default_weight = saved_weights[i] if saved_weights and i < len(saved_weights) else 1.0 / len(tickers)
        with cols[i]:
            w = st.slider(f"{t}", 0.0, 1.0, default_weight, 0.05, key=f"slider_{t}")
            weights.append(w)
    return weights


def plot_portfolio_return(df, key_suffix="fact"):
    rolling = df['Portfolio_Return'].rolling(20).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Portfolio_Return'],
        mode='lines',
        name='Доходность',
        line=dict(color='green')
    ))
    fig.add_trace(go.Scatter(
        x=df.index,
        y=rolling,
        mode='lines',
        name='20-дн. скользящее',
        line=dict(dash='dash', color='gray')
    ))

    fig.update_layout(
        title="Интерактивная доходность портфеля",
        xaxis_title="Дата",
        yaxis_title="Доходность",
        hovermode="x unified",
        template="plotly_white",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True, key=f"portfolio_return_{key_suffix}")



def plot_return_distribution(df, key):
    st.subheader("📊 Распределение дневной доходности")
    fig = px.histogram(
        df,
        x='Portfolio_Return',
        nbins=50,
        title="Гистограмма доходности портфеля",
        labels={'Portfolio_Return': 'Доходность'},
        template="plotly_white"
    )
    fig.update_layout(bargap=0.1)
    st.plotly_chart(fig, use_container_width=True, key=key)


def display_metrics(metrics):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Средняя дневная доходность", f"{metrics['avg_daily_return']:.4%}")
    col2.metric("Стандартное отклонение", f"{metrics['std_dev']:.4%}")
    col3.metric("Коэффициент Шарпа", f"{metrics['sharpe_ratio']:.2f}")
    col4.metric("Доходность за период", f"{metrics['cumulative_return']:.2%}")


def display_asset_statistics(df, tickers, risk_free_rate=0.0):
    st.subheader("📈 Статистика по каждому активу")
    for ticker in tickers:
        price_col = f"{ticker}_Stock_Price"
        return_col = f"{ticker}_Daily_Return"
        if price_col in df.columns and return_col in df.columns:
            avg_return = df[return_col].mean()
            std_dev = df[return_col].std()
            annualized_return = avg_return * 252
            annualized_std = std_dev * (252 ** 0.5)
            sharpe = (annualized_return - risk_free_rate) / annualized_std if annualized_std != 0 else 0
            cumulative = (1 + df[return_col]).prod() - 1

            with st.expander(f"{ticker} - Метрики"):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Средняя доходность", f"{avg_return:.4%}")
                col2.metric("Станд. отклонение", f"{std_dev:.4%}")
                col3.metric("Шарп", f"{sharpe:.2f}")
                col4.metric("Доходность за период", f"{cumulative:.2%}")


def plot_correlation_heatmap(df):
    st.subheader("🧯 Корреляционная матрица доходностей")
    returns_df = df.filter(like="_Daily_Return").dropna(how="any")

    if returns_df.shape[1] < 2 or returns_df.var().sum() == 0:
        st.warning("Недостаточно данных для построения корреляционной матрицы.")
        return

    tickers_order = list(returns_df.columns)
    corr_matrix = returns_df[tickers_order].corr().loc[tickers_order, tickers_order]
    z_values = np.round(corr_matrix.values, 3).tolist()
    annotation_text = [[f"{val:.3f}" for val in row] for row in z_values]

    z_values = z_values[::-1]
    annotation_text = annotation_text[::-1]
    y_labels = tickers_order[::-1]

    fig = ff.create_annotated_heatmap(
        z=z_values,
        x=tickers_order,
        y=y_labels,
        annotation_text=annotation_text,
        colorscale="Viridis",
        showscale=True
    )

    fig.update_layout(
        height=600,
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(size=14)
    )

    st.plotly_chart(fig, use_container_width=True, key="correlation_matrix")


def plot_volatility_function(history):
    st.subheader("📉 Функция волатильности")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(len(history))),
        y=history,
        mode='lines+markers',
        name='Волатильность'
    ))

    fig.update_layout(
        xaxis_title='Итерация',
        yaxis_title='Волатильность портфеля',
        template='plotly_white',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True, key="volatility_function")