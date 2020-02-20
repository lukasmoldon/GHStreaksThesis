# ---------- IMPORT ------------
import logging
import json
import datetime
import matplotlib
import matplotlib.pyplot as plt
# ------------------------------


# ---------- INPUT -------------
path_source = "C:/Users/Lukas/Desktop/results/streakValuesY3MIN50GOAL.json"
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
list_of_datetimes = []
values = []
# ------------------------------



logging.info("Accessing plot data ...")
with open(path_source, "r") as fp:
    plotdata = json.load(fp)

for entry in plotdata:
    list_of_datetimes.append(datetime.datetime.strptime(entry, datetimeFormat).date())
    values.append(plotdata[entry])

logging.info("Done. (1/2)")


logging.info("Creating plot ...")

dates = matplotlib.dates.date2num(list_of_datetimes)
matplotlib.pyplot.plot_date(dates, values, '-')
plt.axvline(x=datetime.datetime.strptime("2016-05-19", datetimeFormat).date(), color='r')
plt.xlabel("Time")
plt.ylabel("Avg. streak length")
plt.show()


logging.info("Done. (2/2)")