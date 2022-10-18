import datetime
import numpy as np
import pandas as pd
import vectorbt as vbt

end_time = datetime.datetime.now()

start_time = end_time - datetime.timedelta(days=3)

btc_price = vbt.YFData.download(
    "BTC-USD",
    missing_index="drop",
    interval = "1min",
    start = start_time,
    end = end_time
).get("Close")


# separar em tempos fixados
btc_price, range_indexes = btc_price.range_split(
    n = 100,
    range_len = 1440
)