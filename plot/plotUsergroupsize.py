# ---------- IMPORT ------------
import logging
import matplotlib
import matplotlib.pyplot as plt
import datetime
import json
import ijson
from datetime import timedelta, date
# ------------------------------


# ---------- INPUT -------------
path_source = "C:/Users/Lukas/Desktop/usergroupsize.json"
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------

# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
plotdata = {}  # key = day, value = usergroupsize
list_of_datetimes = []
values = []
# ------------------------------



log_starttime = datetime.datetime.now()



logging.info("Accessing plotdata ...")
with open(path_source, "r") as fp:
    plotdata = json.load(fp)


logging.info("Creating plot ...")

for day in plotdata:
    list_of_datetimes.append(datetime.datetime.strptime(day, datetimeFormat).date())
    values.append(plotdata[day])

    dates = matplotlib.dates.date2num(list_of_datetimes)
    matplotlib.pyplot.plot_date(dates, values, '-')


plt.axvline(x=datetime.datetime.strptime(
    "2016-05-19", datetimeFormat).date(), color='r')
plt.xlabel("Time")
plt.ylabel("Observed usergroup size")

plt.show()


logging.info("Done. (3/3)")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))