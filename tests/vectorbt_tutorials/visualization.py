import vectorbt as vbt
import datetime

end_date = datetime.datetime.now()

start_date = end_date - datetime.timedelta(days=3)

btc_price = vbt.YFData.download(
    ["BTC-USD"],
    interval = "1m",
    start = start_date,
    end = end_date,
    missing_index= "drop"
).get("Close")

# print(btc_price)

fast_ma = vbt.MA.run(btc_price, window = 50)
slow_ma = vbt.MA.run(btc_price, window = 200)

entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

pf = vbt.Portfolio.from_signals(btc_price, entries, exits)

# pf.plot().show()

# pf.trades.plot_pnl().show()

# print(pf.total_return())

# print(pf.stats())

bbands = vbt.BBANDS.run(btc_price)

# plot in interative window
bbands.plot()