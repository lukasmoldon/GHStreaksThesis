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
path_source = "C:/Users/Lukas/Desktop/mondayStreakValues.json"
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
threshold = 14  # where to cut bar chart and start counting over this threshold?!
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
plotdata = {}  # key = monday type, value = {key = day in observedtime, value = value}
values = []
indices = []
maxlen = 1
avg = 0
overThreshold = 0
observed_mondays = [date(2016, 4, 18), date(2016, 4, 25), date(2016, 5, 2), date(2016, 5, 9), date(
    2016, 5, 16), date(2016, 5, 23), date(2016, 5, 30), date(2016, 6, 6), date(2016, 6, 13), date(2016, 6, 20)]
# ------------------------------


log_starttime = datetime.datetime.now()


logging.info("Accessing plotdata ...")
with open(path_source, "r") as fp:
    plotdata = json.load(fp)


logging.info("Creating plot ...")

fig, ax = plt.subplots()
width = 0.35

values = []
indices = []

length = 1
while length <= threshold:
    indices.append(length - width/2)
    values.append(plotdata["0"][str(length)])
    length += 1

p1 = ax.bar(indices, values, width, align='center')



values = []
indices = []

length = 1
while length <= threshold:
    indices.append(length + width/2)
    values.append(plotdata["8"][str(length)])
    length += 1

p2 = ax.bar(indices, values, width, align='center')


ax.set_xticks(range(1, threshold + 1))
ax.set_xticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
ax.legend((p1[0], p2[0]), (str(observed_mondays[0]), str(observed_mondays[8])))
plt.ylabel("Distribution of streaklengths of streaks starting on both Mondays")
plt.xlabel("\n2016-04-18: Avg streak length: 2.38    Streaks longer than 14: 0.52%\n2016-06-13: Avg streak length: 2.24    Streaks longer than 14: 0.27%")
plt.annotate("Friday peak", xy=(5.1,0.1), xytext=(6,0.15), arrowprops=dict(facecolor='black', shrink=0.03))
plt.annotate("Friday peak", xy=(11.7,0.014), xytext=(8,0.06), arrowprops=dict(facecolor='black', shrink=0.03))
plt.show()


logging.info("Done.")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))
