# -*- coding: utf-8 -*-
import pandas as pd
import datetime as dt
from alpha_vantage.timeseries import TimeSeries
import yfinance as yf

key="RZ9052SXUN5R3GJO"

ts = TimeSeries(key=key, output_format="pandas")

hk_0883 = yf.download(tickers = "0883.HK", start = (dt.datetime.today() - dt.timedelta(58)).strftime("%Y-%m-%d"), end = dt.datetime.today().strftime("%Y-%m-%d") , interval = '15m')
                      
msft, meta_data = ts.get_daily_adjusted(symbol="MSFT", outputsize="full")


def MACD(DF, fast, slow, signal):
    df = DF.copy()
    df.columns = ["open","high","low","close","adjusted_close","volume","dividend","split"]
    df = df[::-1]
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
    df = df[::-1]
    df['H-L'] = abs(df["high"] - df["low"])
    df['H-PC'] = abs(df["high"] - df["adjusted_close"].shift(1))
    df['L-PC'] = abs(df["low"] - df["adjusted_close"].shift(1))
    df['TR'] = df[["H-L", "H-PC", "L-PC"]].max(axis=1, skipna=False)
    df['ATR'] = df["TR"].rolling(n).mean()
    df2 = df.drop(['H-L','H-PC', 'L-PC'], axis=1)
    return df2

def bollinger_band(DF, rolling_days, standard_deviation_multiplier):
    
    """This is a function to calculate the Bollinger Band"""
    
    df = DF.copy()
    #df.columns = ["open", "high", "low", "close", "adjusted_close", "volume", "dividend", "split"]
    #df = df[::-1]
    df["MA"] = df["Adj Close"].rolling(rolling_days).mean()
    df["BB_upper"] = df["MA"] + standard_deviation_multiplier * df["MA"].rolling(rolling_days).std()
    df["BB_lower"] = df["MA"] - standard_deviation_multiplier * df["MA"].rolling(rolling_days).std()
    df["BB_width"] = df["BB_upper"] - df["BB_lower"]
    df.dropna(inplace=True)
    return df

msft_boll = bollinger_band(hk_0883, 20, )

msft_boll.iloc[-150:, [4, 9, 10, -4]].plot()
    



hk_1928 = yf.download(tickers = "1928.HK", period="ytd")
test= hk_1928["Adj Close"].diff()
u = test * 0
d = u.copy()
u[test>0] = test[test>0]
d[test<0] = test[test<0]

boll_0883 = bollinger_band(hk_0883, 20, 3)

boll_0883[["Adj Close", "BB_upper", "BB_lower"]].plot()

hk_0883_1m = yf.download(tickers = "0883.HK", period="7d", interval = "1m")

hk_0883_1m[["Adj Close", "Volume"]].plot(subplots=True)
