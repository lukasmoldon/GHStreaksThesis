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
observed_start = datetime.datetime.strptime("2016-04-28", datetimeFormat).date() # start of observed time, 3 weeks before the change
observed_end = datetime.datetime.strptime("2016-06-09", datetimeFormat).date() # end of observed time, 3 weeks after the change
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
plt.axvline(x=datetime.datetime.strptime("2016-05-19", datetimeFormat).date(), color='r', label="Streaks removed")
plt.xlabel("Time")
plt.ylabel("Number streaks")
plt.legend()
plt.show()


logging.info("Done. (2/2)")