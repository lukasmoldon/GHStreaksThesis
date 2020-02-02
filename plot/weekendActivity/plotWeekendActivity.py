# ---------- IMPORT ------------
import logging
import datetime
import json
from datetime import date, timedelta
import matplotlib
import matplotlib.pyplot as plt
# ------------------------------


# ---------- INPUT -------------
path_source = "C:/Users/Lukas/Desktop/weekendActivity.json"
# ------------------------------


# ---------- OUTPUT ------------
# ------------------------------


# ---------- CONFIG ------------
changemarker = "2016-5-16"
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
x = []
values = []
# ------------------------------



log_starttime = datetime.datetime.now()

with open(path_source, "r") as fp:
    weekdata = json.load(fp)


for index in weekdata:
    x.append(datetime.datetime.strptime(index, datetimeFormat).date())
    values.append(weekdata[index]["RW"])

dates = matplotlib.dates.date2num(x)
matplotlib.pyplot.plot_date(dates, values, '-')

plt.xlabel("Weeks in 2016")
plt.ylabel("Ratio of activity on weekends")
plt.axvline(x=datetime.datetime.strptime(changemarker, datetimeFormat).date(), color='r', label="Streaks removed")

plt.legend()
plt.show()

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))