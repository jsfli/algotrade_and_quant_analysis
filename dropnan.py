# -*- coding: utf-8 -*-

import datetime as dt
import yfinance as yf
import pandas as pd
from alpha_vantage.timeseries import TimeSeries

key_path = "RZ9052SXUN5R3GJO"

ts = TimeSeries(key=key_path, output_format="pandas")

help(ts)

stocks =["AMZN","MSFT","FB",]