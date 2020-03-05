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

avg_before = 0
avg_after = 0
longer_before = 0
longer_after = 0
# ------------------------------


log_starttime = datetime.datetime.now()


logging.info("Accessing plotdata ...")
with open(path_source, "r") as fp:
    plotdata = json.load(fp)



averaged_before = {}
for monday in observed_mondays:
    if monday < date(2016,5,19):
        for length in plotdata[str(monday)]:
            averaged_before[length] = 0

over = 0
cnt = 0
for monday in observed_mondays:
    if monday < date(2016,5,19):
        for length in plotdata[str(monday)]:
            averaged_before[length] += plotdata[str(monday)][length]
            if int(length) <= threshold:
                cnt += plotdata[str(monday)][length]
            else:
                over += plotdata[str(monday)][length]

for length in averaged_before:
    avg_before += averaged_before[length]*int(length)
    averaged_before[length] /= cnt
avg_before /= cnt
longer_before = 100*over/(cnt+over)

averaged_after = {}
for monday in observed_mondays:
    if monday > date(2016,5,19):
        for length in plotdata[str(monday)]:
            averaged_after[length] = 0

over = 0
cnt = 0
for monday in observed_mondays:
    if monday > date(2016,5,19):
        for length in plotdata[str(monday)]:
            averaged_after[length] += plotdata[str(monday)][length]
            if int(length) <= threshold:
                cnt += plotdata[str(monday)][length]
            else:
                over += plotdata[str(monday)][length]

for length in averaged_after:
    avg_after += averaged_after[length]*int(length)
    averaged_after[length] /= cnt
avg_after /= cnt
longer_after = 100*over/(cnt+over)


logging.info("Creating plot ...")

fig, ax = plt.subplots()
width = 0.35

values = []
indices = []

length = 1
while length <= threshold:
    indices.append(length - width/2)
    values.append(averaged_before[str(length)])
    length += 1

p1 = ax.bar(indices, values, width, align='center', color="#17719B")



values = []
indices = []

length = 1
while length <= threshold:
    indices.append(length + width/2)
    values.append(averaged_after[str(length)])
    length += 1

p2 = ax.bar(indices, values, width, align='center', color="#32A875")


ax.set_xticks(range(1, threshold + 1))
ax.set_xticklabels(["1 \n(Mon)", "2 \n(Tue)", "3 \n(Wed)", "4 \n(Thu)", "5 \n(Fri)", "6 \n(Sat)", "7 \n(Sun)", "8 \n(Mon)", "9 \n(Tue)", "10 \n(Wed)", "11 \n(Thu)", "12 \n(Fri)", "13 \n(Sat)", "14 \n(Sun)"])
ax.legend((p1[0], p2[0]), ("Before (avg)", "After (avg)"))
plt.ylabel("Share of streaks", fontsize=12)
plt.xlabel("Streak length in days (endpoint)\nBefore: Avg streak length: " + str(round(avg_before, 2)) + "    Streaks longer than 14:  " + str(round(longer_before, 2))+ "%" + 
            "\nAfter: Avg streak length:  " + str(round(avg_after, 2)) + "    Streaks longer than 14:  " + str(round(longer_after, 2)) + "%")
plt.annotate("Friday peak", xy=(5.1,0.1), xytext=(6,0.15), arrowprops=dict(facecolor='black', shrink=0.03))
plt.annotate("Friday peak", xy=(11.7,0.014), xytext=(8,0.06), arrowprops=dict(facecolor='black', shrink=0.03))
plt.show()


logging.info("Done.")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))
