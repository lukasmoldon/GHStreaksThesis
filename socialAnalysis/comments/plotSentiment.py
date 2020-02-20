# ---------- IMPORT ------------
import logging
import datetime
import json
import datetime
from datetime import timedelta, date
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# ------------------------------


# ---------- INPUT -------------
path_source = "C:/Users/Lukas/Desktop/commentSentiment.json"
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
observed_start = date(2016,1,1)
observed_end = date(2017,1,1)

mode = "neg" # "avg" = average sent, "neg" = negative sentiment
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
list_of_datetimes = []
values = []
# ------------------------------



def daterange(observedtime_start, observedtime_end):
        for n in range(int((observedtime_end - observedtime_start).days + 1)):
                yield observedtime_start + timedelta(n)


log_starttime = datetime.datetime.now()


logging.info("Loading data ...")
with open(path_source, "r") as fp:
    data_raw = json.load(fp)
logging.info("Done (1/2)")


logging.info("Computing ...")

data = {}

if mode == "avg":
    cnt = 0
    for rowindex in data_raw:
        cnt += 1
        if (cnt%1000000 == 0): logging.info(str(cnt/1000000) + " million observations computed")
        if data_raw[rowindex]["sentiment"] > 0.1 or data_raw[rowindex]["sentiment"] < -0.1:
            if data_raw[rowindex]["timestamp"] in data:
                data[data_raw[rowindex]["timestamp"]]["sum"] += data_raw[rowindex]["sentiment"]
                data[data_raw[rowindex]["timestamp"]]["cnt"] += 1
            else:
                data[data_raw[rowindex]["timestamp"]] = {
                    "sum": data_raw[rowindex]["sentiment"],
                    "cnt": 1,
                    "avg": 0
                }

    for day in data:
        if data[day]["cnt"] > 0:
            data[day]["avg"] = (data[day]["sum"]/data[day]["cnt"])


    for day in daterange(observed_start, observed_end):
        list_of_datetimes.append(day)
        if str(day) in data:
            values.append(data[str(day)]["avg"])
        else:
            values.append(0)

    dates = matplotlib.dates.date2num(list_of_datetimes)
    matplotlib.pyplot.plot_date(dates, values, '-')
    plt.xlabel("Time")
    plt.ylabel("Avg. sentiment")
    plt.axvline(x=datetime.datetime.strptime("2016-05-19", datetimeFormat).date(), color='r', label="Streaks removed")
    plt.legend()
    plt.show()

elif mode == "neg":
    cnt = 0
    for rowindex in data_raw:
        cnt += 1
        if (cnt%1000000 == 0): logging.info(str(cnt/1000000) + " million observations computed")
        if data_raw[rowindex]["sentiment"] < -0.8:
            if data_raw[rowindex]["timestamp"] in data:
                data[data_raw[rowindex]["timestamp"]]["cnt"] += 1
            else:
                data[data_raw[rowindex]["timestamp"]] = {
                    "cnt": 1
                }

    for day in daterange(observed_start, observed_end):
        list_of_datetimes.append(day)
        if str(day) in data:
            values.append(data[str(day)]["cnt"])
        else:
            values.append(0)

    dates = matplotlib.dates.date2num(list_of_datetimes)
    matplotlib.pyplot.plot_date(dates, values, '-')
    plt.xlabel("Time")
    plt.ylabel("Amount of negative sentiment")
    plt.axvline(x=datetime.datetime.strptime("2016-05-19", datetimeFormat).date(), color='r', label="Streaks removed")
    plt.legend()
    plt.show()





logging.info("Done (2/2)")



log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))