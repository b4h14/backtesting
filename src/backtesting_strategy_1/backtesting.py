import datetime
import numpy as np
import pandas as pd
import vectorbt as vbt
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go


"""
Módulo que gera os backtestings salvando-os em arquivos para comparação.

Aqui usamos uma estratégia com rsi com uma janela de 21

"""

end_time = datetime.datetime.now()

start_time = end_time - datetime.timedelta(days=365)

# Não encontrei o código da Refinaria Riograndense.

list_stock_enterprises = [
    'RRRP3.SA', 
    'CSAN3.SA', 
    'DMMO3.SA', 
    'ENAT3.SA', 
    'PRIO3.SA',
    'PETR3.SA',
    'RECV3.SA',
    'RPMG3.SA',
    'UGPA3.SA',
    'VBBR3.SA',

    ]

def plot_bbands(vbt_stock, stock_enterprise):
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

    name = f"{stock_enterprise}_bbands.pdf"
    pio.write_image(fig, name)

    return fig.show()

    """
    O loop a seguir gera os arquivos de backtesting em formato .csv e exporta os plots em .pdf/no navegador

    """


for stock_enterprise in list_stock_enterprises:
    b3_petroleum = vbt.YFData.download(
    stock_enterprise,
    missing_index="drop",
    interval = "1d",
    start = start_time,
    end = end_time
    )

    stock_prices = b3_petroleum.get("Close")

    rsi = vbt.RSI.run(stock_prices, window = 21)

    entries = rsi.rsi_crossed_below(30)

    exits = rsi.rsi_crossed_above(70)

    pf = vbt.Portfolio.from_signals(stock_prices, entries, exits)

    with open(f'{stock_enterprise}.csv','w') as f:
        f.write(pf.stats().to_string())

    plot_bbands(b3_petroleum, stock_enterprise)    



