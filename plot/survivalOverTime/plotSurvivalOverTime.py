# ---------- IMPORT ------------
import logging
import datetime
from datetime import date, timedelta
import json
import matplotlib
import matplotlib.pyplot as plt
# ------------------------------


# ---------- INPUT -------------
path_source = "C:/Users/Lukas/Desktop/survivalOverTime.json"
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
a = 20
b = 120

observed_weeks = [
    date(2016, 1, 4), 
    date(2016, 1, 11),
    date(2016, 1, 18), 
    date(2016, 1, 25), 
    date(2016, 2, 1), 
    date(2016, 2, 8), 
    date(2016, 2, 15), 
    date(2016, 2, 22), 
    date(2016, 2, 29), 
    date(2016, 3, 7),
    date(2017, 1, 2), 
    date(2017, 1, 9),
    date(2017, 1, 16), 
    date(2017, 1, 23), 
    date(2017, 1, 30), 
    date(2017, 2, 6), 
    date(2017, 2, 13), 
    date(2017, 2, 20), 
    date(2017, 2, 27), 
    date(2017, 3, 6)
    ]
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
changedate = date(2016, 5, 19)
# ------------------------------



log_starttime = datetime.datetime.now()

logging.info("Loading data ...")
with open(path_source, "r") as fp:
    plotdata = json.load(fp)
logging.info("Done (1/2)")


logging.info("Starting ...")

for week in observed_weeks:

    week = str(week)

    total = plotdata[week]["1"]
    for day in plotdata[week]:
        plotdata[week][day] /= total
            
    start = datetime.datetime.strptime(week, datetimeFormat).date()
    x = []
    values = []
    for day in plotdata[week]:
        if int(day) <= b and int(day) >= a:
            x.append(int(day))
            values.append(plotdata[week][day])
    if start < changedate:
        plt.plot(x, values, '-', color="#17719B", linewidth=1.3)
    else:
        plt.plot(x, values, '-', color='#D3685D', linewidth=1.3)

x = []
values = []
plt.plot(x, values, '-', color="#17719B", label="Before")
plt.plot(x, values, '-', color='#D3685D', label="After")
plt.xlabel("Days", fontsize=13)
plt.ylabel("Share of streaks surviving at least x days", fontsize=13)
plt.legend(fontsize=11)
plt.show()

logging.info("Done (2/2)")





log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))