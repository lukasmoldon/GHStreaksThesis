# ---------- IMPORT ------------
import logging
import json
import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import colorConverter as cc
import numpy as np
# ------------------------------


# ---------- INPUT -------------
path_source = "C:/Users/Lukas/Desktop/streakSurvivalRatesMIN30.json"
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
datetimeFormat = "%Y-%m-%d"
observed_start = datetime.datetime.strptime("2016-01-01", datetimeFormat).date()
observed_end = datetime.datetime.strptime("2017-01-01", datetimeFormat).date()
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
list_of_datetimes = []
valuesActive = []
valuesAbandoned = []
# ------------------------------



logging.info("Accessing plot data ...")
with open(path_source, "r") as fp:
    plotdata = json.load(fp)

for entry in plotdata:
    timestamp = datetime.datetime.strptime(entry, datetimeFormat).date()
    if timestamp >= observed_start and timestamp <= observed_end:
        list_of_datetimes.append(timestamp)
        valuesActive.append(plotdata[entry]["1"])
        valuesAbandoned.append(plotdata[entry]["0"])


dates = matplotlib.dates.date2num(list_of_datetimes)
logging.info("Done. (1/2)")


logging.info("Creating plot ...")

matplotlib.pyplot.plot_date(dates, valuesActive, '-', label="Active")
matplotlib.pyplot.plot_date(dates, valuesAbandoned, '-', label="Abandoned")
plt.axvline(x=datetime.datetime.strptime("2016-02-15", datetimeFormat).date(), color='c', label="President's day 2016")
plt.axvline(x=datetime.datetime.strptime("2016-05-19", datetimeFormat).date(), color='r', label="Streaks removed")
plt.axvline(x=datetime.datetime.strptime("2016-05-30", datetimeFormat).date(), color='y', label="Memorial Day 2016")
plt.axvline(x=datetime.datetime.strptime("2016-07-04", datetimeFormat).date(), color='g', label="Independence Day 2016")
plt.axvline(x=datetime.datetime.strptime("2016-09-05", datetimeFormat).date(), color='c', label="Labor Day 2016")
plt.axvline(x=datetime.datetime.strptime("2016-11-11", datetimeFormat).date(), color='m', label="Veteran's Day 2016")
plt.axvline(x=datetime.datetime.strptime("2016-12-06", datetimeFormat).date(), color='k', label="GitHub Major Service Outage")
plt.axvline(x=datetime.datetime.strptime("2016-12-25", datetimeFormat).date(), color='b', label="Christmas 2016")
plt.xlabel("Time")
plt.ylabel("Number streaks")
plt.legend()
plt.show()


logging.info("Done. (2/2)")