# -*- coding: utf-8 -*-

from alpha_vantage.techindicators import TechIndicators 
import pandas as pd
import datetime as dt
import time
import os

key_path = "RZ9052SXUN5R3GJO"

ti = TechIndicators(key = key_path, output_format = "pandas")

gbpusd_50_sma, meta_data = ti.get_sma("CNYUSD", interval = "60min", time_period=50, series_type="close")

gbpusd_50_sma.columns = ["50 SMA"]

gbpusd_50_sma["50 SMA"].plot()

gbpusd_200_sma, meta_data = ti.get_sma("CNYUSD", interval = "60min", time_period=200, series_type="close")

gbpusd_200_sma.columns = ["200 SMA"]

gbpusd = pd.concat([gbpusd_50_sma, gbpusd_200_sma], axis=1)

gbpusd.plot()

