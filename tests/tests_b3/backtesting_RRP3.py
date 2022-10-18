import numpy as np
import pandas as pd
import vectorbt as vbt
import plotly.graph_objects as go

"""
Módulo que testa a atividade proposta de backtesting a partir de 1 ano com diferentes
estratégias.

"""


end_time = '2022-09-30'

start_time = '2021-09-30'

RRRP3 = vbt.YFData.download(
    "RRRP3.SA",
    missing_index="drop",
    interval = "1d",
    start = start_time,
    end = end_time
)

RRRP3_price = RRRP3.get("Close")

def plot_bbands(vbt_stock):
    """
    Plots the BBANDS of a vbt object.
    """
    df = vbt_stock.get().reset_index()

    for i in ['Open', 'High', 'Close', 'Low']:
        df[i]  =  df[i].astype('float64')

    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                        close=df['Close'])])

    return fig.show()

plot_bbands(RRRP3)

# but also using the native plot_bbands function instead

bbands = vbt.BBANDS.run(RRRP3_price)

# using jupyter
bbands.plot()

################################################################

# rsi strategy
"""rsi = vbt.RSI.run(RRRP3_price, window = 21)

entries = rsi.rsi_crossed_below(30)

exits = rsi.rsi_crossed_above(70)

pf = vbt.Portfolio.from_signals(RRRP3_price, entries, exits)

print(pf.stats())

pf.plot().show()"""

################################################################

# Dual Moving Average Crossover (DMAC) strategy in 1y interval 
# (250 working days)

"""fast_ma = vbt.MA.run(RRRP3_price, window = 50)
slow_ma = vbt.MA.run(RRRP3_price, window = 200)

entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

pf = vbt.Portfolio.from_signals(RRRP3_price, entries, exits)

print(pf.stats())
pf.plot().show()"""

################################################################

# random combinations strategy with parameter optimization

windows = np.arange(2, 101)
fast_ma, slow_ma = vbt.MA.run_combs(RRRP3_price, window=windows, r=2, short_names=['fast', 'slow'])
entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

pf_kwargs = dict(size=np.inf, fees=0.001, freq='1D')
pf = vbt.Portfolio.from_signals(RRRP3_price, entries, exits, **pf_kwargs)

returns = pf.total_return()

print(returns.max())
print(returns.idxmax()) # (9,10)

pf[returns.idxmax()].stats()

pf[returns.idxmax()].plot().show()
