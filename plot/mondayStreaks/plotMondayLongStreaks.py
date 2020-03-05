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
path_source = "C:/Users/Lukas/Desktop/mondayLongStreakValues.json"
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
observed_start = 8 # range of bar chart AND calculation
observed_end = 21 # range of bar chart AND calculation
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
plotdata = {}  # key = monday type, value = {key = day in observedtime, value = value}
values = []
indices = []
avg = 0
cnt_streaks = 0
observed_mondays = [
    date(2016, 1, 4), 
    date(2016, 1, 11),
    date(2016, 1, 18), 
    date(2016, 1, 25), 
    date(2016, 2, 1), 
    date(2016, 2, 8), 
    date(2016, 2, 15), 
    date(2016, 2, 22), 
    date(2016, 2, 29), 
    date(2016, 3, 7)
    ]
# ------------------------------



log_starttime = datetime.datetime.now()


logging.info("Accessing plotdata ...")
with open(path_source, "r") as fp:
    plotdata = json.load(fp)

averaged = {}
for monday in observed_mondays:
    for length in plotdata[str(monday)]:
        averaged[length] = 0

cnt = 0
for monday in observed_mondays:
    for length in plotdata[str(monday)]:
        averaged[length] += plotdata[str(monday)][length]
        if int(length) >= observed_start and int(length) <= observed_end:
            cnt += plotdata[str(monday)][length]

for length in averaged:
    averaged[length] /= cnt


logging.info("Creating plot ...")

values = []
indices = []
avg = 0
cnt_streaks = 0

for length in averaged:
    if int(length) >= observed_start and int(length) <= observed_end:
        cnt_streaks += averaged[length]
        avg += (averaged[length] * int(length))
        
avg = (avg / cnt_streaks)

length = observed_start
while length <= observed_end:
    indices.append(length)
    if str(length) in averaged:
        values.append(averaged[str(length)])
    else:
        values.append(0)
    length += 1


matplotlib.pyplot.bar(indices, values, color="#17719B")
plt.xlabel("Streak length in days" + "     (Avg streak length: " + str(round(avg, 2)) + ")", fontsize=12)
plt.xticks(range(observed_start, observed_end + 1), labels=["Mon\n(8)", "Tue\n(9)", "Wed\n(10)", "Thu\n(11)", "Fri\n(12)", "Sat\n(13)", "Sun\n(14)", "Mon\n(15)", "Tue\n(16)", "Wed\n(17)", "Thu\n(18)", "Fri\n(19)", "Sat\n(20)", "Sun\n(21)"])
plt.ylabel("Share of streaklengths > 7", fontsize=12)
plt.annotate("Friday peak", xy=(12.5,0.19), xytext=(14.5,0.16), arrowprops=dict(facecolor='black', shrink=0.03))
plt.annotate("Friday peak", xy=(18.7,0.04), xytext=(14.7,0.07), arrowprops=dict(facecolor='black', shrink=0.03))
plt.show()
    


logging.info("Done.")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))