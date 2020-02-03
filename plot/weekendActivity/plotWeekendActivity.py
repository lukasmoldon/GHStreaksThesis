# ---------- IMPORT ------------
import logging
import datetime
import json
from datetime import date, timedelta
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
# ------------------------------


# ---------- INPUT -------------
path_source = "C:/Users/Lukas/Desktop/weekendActivity.json"
# ------------------------------


# ---------- OUTPUT ------------
# ------------------------------


# ---------- CONFIG ------------
observed_start = date(2016,1,1)
observed_end = date(2016,12,31)
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
x = []
values = []
changedate = date(2016,5,16)
beforeavg = []
afteravg = []
# ------------------------------



log_starttime = datetime.datetime.now()

with open(path_source, "r") as fp:
    weekdata = json.load(fp)


for index in weekdata:
    timestamp = datetime.datetime.strptime(index, datetimeFormat).date()
    if timestamp >= observed_start and timestamp <= observed_end:
        x.append(timestamp)
        values.append(weekdata[index]["RW"])
        if timestamp <= changedate:
            beforeavg.append(weekdata[index]["RW"])
        else:
            afteravg.append(weekdata[index]["RW"])

dates = matplotlib.dates.date2num(x)
matplotlib.pyplot.plot_date(dates, values, '-')

plt.xlabel("Weeks in 2016")
plt.ylabel("Ratio of activity on weekends")
plt.axvline(x=changedate, color='r', label="Streaks removed")
plt.hlines(y=np.mean(beforeavg), xmin=observed_start, xmax=changedate, color='b', label="Mean before = " + str(round(np.mean(beforeavg), 3)))
plt.hlines(y=np.mean(afteravg), xmin=changedate, xmax=observed_end, color='b', label="Mean after = " + str(round(np.mean(afteravg), 3)))

plt.legend()
plt.show()

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))