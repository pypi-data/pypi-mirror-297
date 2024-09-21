import backtrader as bt
import numpy as np
import dash
from dash import dash_table
from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def run_and_show_performance(cerebro, debug=False):
    if hasattr(cerebro, 'runstrats'):
        raise Exception('Cerebro already run. Cannot run again')

    add_analyzers(cerebro, debug)
    show_performance(cerebro.run(), debug)

def add_observers(cerebro, debug=False):
    cerebro.addobserver(bt.observers.BuySell)

def add_analyzers(cerebro, debug=False):
    cerebro.addanalyzer(bt.analyzers.Returns, 
                        _name='returns', 
                        timeframe=bt.TimeFrame.Minutes, 
                        compression=1,
                        tann=252 * 6.5 * 60)

    cerebro.addanalyzer(bt.analyzers.TimeReturn, 
                        _name='timereturn',
                        timeframe=bt.TimeFrame.Minutes, 
                        compression=1)

    cerebro.addanalyzer(bt.analyzers.SharpeRatio, 
                        _name='sharpe',
                        timeframe=bt.TimeFrame.Minutes,
                        compression=1,
                        annualize=True)

    cerebro.addanalyzer(bt.analyzers.DrawDown, 
                        _name='drawdown')
    
def add_metrics_plot(strat, views, debug=False):
    returns = strat.analyzers.returns.get_analysis()
    if debug:
        print(f"Total Compound Return: {returns['rtot']:.2%}, Annualized Return: {returns['rnorm']:.2%}")

    sharpe = strat.analyzers.sharpe.get_analysis()
    if debug and sharpe['sharperatio'] is not None:
        print(f"Sharpe Ratio: {sharpe['sharperatio']:.2f}")

    timereturn = strat.analyzers.timereturn.get_analysis()
    print(timereturn)
    timereturn_list = list(timereturn.values())
    volatility = np.std(timereturn_list)
    annual_volatility = volatility * np.sqrt(252)
    if debug:
        print(f"Annualized Volatility: {annual_volatility:.2%}")

    drawdown = strat.analyzers.drawdown.get_analysis()
    if debug:
        print(f"Max Drawdown: {drawdown.max.drawdown:.2f}%, Max Drawdown Duration: {drawdown.max.len}")

    # Metrics Table
    metrics_data = {
        "Metrics": [
            "Total Compound Return", 
            "Annualized Return", 
            "Sharpe Ratio", 
            "Annualized Volatility", 
            "Max Drawdown", 
            "Max Drawdown Duration"
        ],
        "Result": [
            f"{returns['rtot']:.2%}", 
            f"{returns['rnorm']:.2%}", 
            f"{sharpe['sharperatio']:.2f}" if sharpe['sharperatio'] is not None else "NA", 
            f"{annual_volatility:.2%}",
            f"{drawdown.max.drawdown:.2f}%",
            f"{drawdown.max.len}"
        ]
    }
    metrics_df = pd.DataFrame(metrics_data)
    views.append(html.H2("Overall Metrics"))
    views.append(dash_table.DataTable(
            data=metrics_df.to_dict('records'),
            style_cell={'textAlign': 'left'},
            style_header={
                'backgroundColor': 'lightgrey',
                'fontWeight': 'bold'
            },
            style_cell_conditional=[
                {'if': {'column_id': 'Metrics'}, 'width': '50%'},
                {'if': {'column_id': 'Result'}, 'width': '50%'}
            ]
    ))

def add_portfolio_plot(strat, views, debug=False):
    # Portfolio Value
    for observer in strat.observers:
        if isinstance(observer, bt.observers.Broker):
            portfolio_values = []
            length = observer.lines.value.__len__()
            for i in range(0, length):
                portfolio_values.append(observer.lines.value.__getitem__(0 -(length - 1 - i)))
            dates = [bt.num2date(d) for d in strat.datas[0].datetime.get(size=len(portfolio_values))]

            df = pd.DataFrame({'Date': dates, 'Portfolio Value': portfolio_values})
            if debug:
                print(f"portfolio df: {df}")
            fig = px.line(df, x='Date', y='Portfolio Value')
            views.append(html.H2("Portfolio Value(Including Cash)"))
            views.append(dcc.Graph(figure=fig))

def add_buysell_plot(strat, views, debug=False):
    # Buy/Sell Points
    market_data = strat.datas[0]
    market_data_length = len(market_data)
    data_df = pd.DataFrame({
        'Date': [market_data.datetime.datetime(0 - (market_data_length - 1 - i)) for i in range(market_data_length)],
        'Open': [market_data.open[0 - (market_data_length - 1 - i)] for i in range(market_data_length)],
        'High': [market_data.high[0 - (market_data_length - 1 - i)] for i in range(market_data_length)],
        'Low': [market_data.low[0 - (market_data_length - 1 - i)] for i in range(market_data_length)],
        'Close': [market_data.close[0 - (market_data_length - 1 - i)] for i in range(market_data_length)]
    })
    if debug:
        print(f"candlestick df: {data_df}")
    fig = go.Figure(
        go.Candlestick(
            x=data_df["Date"],
            open=data_df["Open"],
            high=data_df["High"],
            low=data_df["Low"],
            close=data_df["Close"],
        )
    )
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=True
    )
    for observer in strat.observers:
        if isinstance(observer, bt.observers.BuySell):
            dates = [bt.num2date(d) for d in strat.datas[0].datetime.get(size=market_data_length)]
            buy_prices = []
            buy_dates = []
            length = observer.lines.buy.__len__()
            for i in range(0, length):
                p = observer.lines.buy.__getitem__(0 -(length - 1 - i))
                if isinstance(p, (int, float)):
                    buy_prices.append(p)
                    buy_dates.append(dates[i])
            sell_prices = []
            sell_dates = []
            length = observer.lines.sell.__len__()
            for i in range(0, length):
                p = observer.lines.sell.__getitem__(0 -(length - 1 - i))
                if isinstance(p, (int, float)):
                    sell_prices.append(p)
                    sell_dates.append(dates[i])
            fig.add_trace(
                go.Scatter(
                    x=buy_dates, 
                    y=buy_prices, 
                    mode="markers", 
                    marker=dict(symbol="triangle-up", color="blue", size=18),
                    name="Buy Points"
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=sell_dates, 
                    y=sell_prices, 
                    mode="markers", 
                    marker=dict(symbol="triangle-down", color="black", size=18),
                    name="Sell Points"
                )
            )
    views.append(html.H2("Buy/Sell Points"))
    views.append(dcc.Graph(figure=fig))

def show_performance(strats, debug=False):
    for strat in strats:
        views = []
        add_metrics_plot(strat, views, debug)
        add_portfolio_plot(strat, views, debug)
        add_buysell_plot(strat, views, debug)

        app = dash.Dash(__name__)
        app.layout = html.Div(views)

        app.run_server(host='0.0.0.0', 
            port=8050, 
            jupyter_mode="jupyterlab",
            jupyter_server_url="http://192.168.25.144:8050", 
            debug=True
        )