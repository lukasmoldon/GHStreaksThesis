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
observed_start = 7  # range of bar chart AND calculation
observed_end = 35  # range of bar chart AND calculation
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
plotdata = {}  # key = monday type, value = {key = day in observedtime, value = value}
values = []
indices = []
avg = 0
observed_mondays = [date(2016, 4, 11), date(2016, 4, 18), date(2016, 4, 25), date(2016, 5, 2), date(2016, 5, 9), date(
    2016, 5, 16), date(2016, 5, 23), date(2016, 5, 30), date(2016, 6, 6), date(2016, 6, 13), date(2016, 6, 20), date(2016, 6, 27)]
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
avg = 0
cnt_streaks = 0

for length in plotdata["0"]:
    if int(length) >= observed_start and int(length) <= observed_end:
        cnt_streaks += plotdata["0"][str(length)]
        avg += (plotdata["0"][str(length)] * int(length))

    
avg = (avg / cnt_streaks)

length = observed_start
while length <= observed_end:
    indices.append(length - width/2)
    if str(length) in plotdata["0"]:
        values.append(plotdata["0"][str(length)] / cnt_streaks)
    else:
        values.append(0)
    length += 1


p1 = ax.bar(indices, values, width, align='center')




values = []
indices = []
avgI = 0
cnt_streaks = 0

for length in plotdata["6"]:
    if int(length) >= observed_start and int(length) <= observed_end:
        cnt_streaks += plotdata["6"][str(length)]
        avgI += (plotdata["6"][str(length)] * int(length))

    
avgI = (avgI / cnt_streaks)

length = observed_start
while length <= observed_end:
    indices.append(length + width/2)
    if str(length) in plotdata["6"]:
        values.append(plotdata["6"][str(length)] / cnt_streaks)
    else:
        values.append(0)
    length += 1

p2 = ax.bar(indices, values, width, align='center')


ax.set_xticks(range(observed_start, observed_end + 1))
ax.legend((p1[0], p2[0]), (str(observed_mondays[0]), str(observed_mondays[6])))
plt.ylabel("Distribution of streaklengths of streaks starting on both Mondays")
plt.xlabel("\n" + str(observed_mondays[0]) + ": Avg streak length: " + str(round(avg, 2)) + "\n" + str(observed_mondays[6]) + ": Avg streak length: " + str(round(avgI, 2)))

plt.show()


logging.info("Done.")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))
