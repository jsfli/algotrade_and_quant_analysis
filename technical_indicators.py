# -*- coding: utf-8 -*-
import pandas as pd
import datetime as dt
from alpha_vantage.timeseries import TimeSeries

key="RZ9052SXUN5R3GJO"

ts = TimeSeries(key=key, output_format="pandas")

msft, meta_data = ts.get_daily_adjusted(symbol="MSFT", outputsize="full")


def MACD(DF, fast, slow, signal):
    df = DF.copy()
    df.columns = ["open","high","low","close","adjusted_close","volume","dividend","split"]
    df["MACD_Fast"] = df["adjusted_close"].ewm(span=fast, min_periods=fast).mean()
    df["MACD_Slow"] = df["adjusted_close"].ewm(span=slow, min_periods=slow).mean()
    df["MACD"] = df["MACD_Fast"] - df["MACD_Slow"]
    df["MACD_Signal"] = df["MACD"].ewm(span=signal, min_periods=signal).mean()
    df.dropna(inplace=True)
    return df

def ATR(DF, n):
    """
    This is a function to calculate the True Range
    and Average True Range
    """
    df = DF.copy()
    df.columns = ["open", "high", "low", "close", "adjusted_close", "volume", "dividend", "split"]
    df["H-L"] = abs(df["high"] - df["low"])
    df["H-PC"] = abs(df["high"] - df["adjusted_close"].shift(1))
    df["L-PC"] = abs(df["low"] - df["adjusted_close"].shift(1))
    df["TR"] = df[["H-L"],["H-PC"],["L-PC"]].max(axis=1, skipna=False)
    df["ATR"] = df["TR"].rolling(n).mean()
    df2 = df.drop(["H-L","H-PC", "L-PC"], axis=1)
    return df2