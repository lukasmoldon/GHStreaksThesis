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
observed_start = 15  # range of bar chart AND calculation
observed_end = 100  # range of bar chart AND calculation
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
plotdata = {}  # key = monday type, value = {key = day in observedtime, value = value}
values = []
indices = []
bins = [(15, 34), (35, 54), (55, 74), (75, 100)]
binval = [0, 0, 0, 0]
avg = 0
observed_mondays = [date(2016, 4, 6), date(2016, 4, 18), date(2016, 4, 25), date(2016, 5, 2), date(2016, 5, 9), date(
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

for length in plotdata["1"]:
    if int(length) >= observed_start and int(length) <= observed_end:
        cnt_streaks += plotdata["1"][str(length)]
        avg += (plotdata["1"][str(length)] * int(length))

    
avg = (avg / cnt_streaks)



i = observed_start
while i <= observed_end:
    if str(i) in plotdata["1"]:
        for el in bins:
            if i >= el[0] and i <= el[1]:
                binval[bins.index(el)] += plotdata["1"][str(i)]
    i += 1

i = 1
while i <= len(bins):
    indices.append(i - width/2)
    values.append(binval[i-1]/cnt_streaks)
    i += 1

p1 = ax.bar(indices, values, width, align='center')




values = []
indices = []
avgI = 0
cnt_streaks = 0
binval = [0, 0, 0, 0]

for length in plotdata["9"]:
    if int(length) >= observed_start and int(length) <= observed_end:
        cnt_streaks += plotdata["9"][str(length)]
        avgI += (plotdata["9"][str(length)] * int(length))


avgI = (avgI / cnt_streaks)

i = observed_start
while i <= observed_end:
    if str(i) in plotdata["9"]:
        for el in bins:
            if i >= el[0] and i <= el[1]:
                binval[bins.index(el)] += plotdata["9"][str(i)]
    i += 1



i = 1
while i <= len(bins):
    indices.append(i + width/2)
    values.append(binval[i-1]/cnt_streaks)
    i += 1


p2 = ax.bar(indices, values, width, align='center')


ax.set_xticks([1,2,3,4])
ax.set_xticklabels(["15 - 34", "35 - 54", "55 - 74", "75 - 100"])
ax.legend((p1[0], p2[0]), (str(observed_mondays[1]), str(observed_mondays[9])))
plt.ylabel("Distribution of streaklengths starting on both Mondays")
plt.xlabel("\n" + str(observed_mondays[1]) + ": Avg streak length: " + str(round(avg, 2)) + "\n" + str(observed_mondays[9]) + ": Avg streak length: " + str(round(avgI, 2)))
plt.annotate("No streaks with length >54\nafter the design change", xy=(3.1,0.07), xytext=(2.6,0.2), arrowprops=dict(facecolor='black', shrink=0.03))
plt.show()


logging.info("Done.")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))
