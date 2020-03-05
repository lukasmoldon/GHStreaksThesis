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
observed_start = date(2016,2,1)
observed_end = date(2016,10,1)
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
x = []
values = []
changedate = date(2016,5,16) # 16th may for monday before the change
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
matplotlib.pyplot.plot_date(dates, values, '-', color='#17719B')

plt.xlabel("Weeks in 2016", fontsize=13)
plt.ylabel("Ratio of activity on weekends", fontsize=13)
plt.axvline(x=datetime.datetime.strptime("2016-05-16", datetimeFormat).date(), color='#D3685D', label="Design change") # 16th may for monday before the change
plt.axvline(x=datetime.datetime.strptime("2016-07-04", datetimeFormat).date(), color="#8C8C8C", ls=":", label="Independence Day")
#plt.axvline(x=date(2016,12,25), color='g', label="Christmas")
plt.hlines(y=np.mean(beforeavg), xmin=observed_start, xmax=changedate, color='#17719B', label="Mean before = " + str(round(np.mean(beforeavg), 3)))
plt.hlines(y=np.mean(afteravg), xmin=changedate, xmax=observed_end, color='#17719B', label="Mean after = " + str(round(np.mean(afteravg), 3)))

plt.legend(fontsize=11)
plt.show()

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))