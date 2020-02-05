# ---------- IMPORT ------------
import logging
import datetime
import json
import datetime
from datetime import timedelta, date
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
# ------------------------------


# ---------- INPUT -------------
path_source = "C:/Users/Lukas/Desktop/issueCommentsCount.json"

path_source_communitysize = "C:/Users/Lukas/Desktop/communitysize_per_day.json"
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
observed_start = date(2012,1,1)
observed_end = date(2019,1,1)
total = False # total count or per user
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
data = {}
list_of_datetimes = []
values = []
# ------------------------------


def daterange(observedtime_start, observedtime_end):
        for n in range(int((observedtime_end - observedtime_start).days + 1)):
                yield observedtime_start + timedelta(n)


log_starttime = datetime.datetime.now()


logging.info("Loading data ...")
with open(path_source, "r") as fp:
    data = json.load(fp)
with open(path_source_communitysize, "r") as fp:
    community = json.load(fp)
logging.info("Done (1/2)")


logging.info("Starting ...")

for day in daterange(observed_start, observed_end):
    list_of_datetimes.append(day)
    if str(day) in data:
        if total:
            values.append(data[str(day)])
        else:
            values.append(data[str(day)]/community[str(day)])
    else:
        values.append(0)

dates = matplotlib.dates.date2num(list_of_datetimes)
matplotlib.pyplot.plot_date(dates, values, '-')
plt.axvline(x=datetime.datetime.strptime("2016-05-19", datetimeFormat).date(), color='r')
plt.xlabel("Time")
if total:
    plt.ylabel("Total number of comments on issues per day")
else:
    plt.ylabel("Number of comments on issues per user per day")
plt.show()

logging.info("Done (2/2)")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))