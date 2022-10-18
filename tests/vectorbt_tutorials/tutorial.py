import vectorbt as vbt
import datetime

end_date = datetime.datetime.now()

start_date = end_date - datetime.timedelta(days=365)

btc_price = vbt.YFData.download(
    ["VBBR3.SA"],
    interval = "1d",
    start = start_date,
    end = end_date,
    missing_index='drop'
).get("Close")

rsi = vbt.RSI.run(btc_price, window = 14)

entries = rsi.rsi_crossed_below(30)

exits = rsi.rsi_crossed_above(70)

pf = vbt.Portfolio.from_signals(btc_price, entries, exits)

pf.plot().show()
