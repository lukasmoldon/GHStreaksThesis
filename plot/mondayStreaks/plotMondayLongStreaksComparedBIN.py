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
observed_mondays = [date(2016, 1, 18), date(2016, 2, 1), date(2016, 2, 15), date(2017, 1, 16), date(2017, 1, 30), date(2017, 2, 13)]

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
            if int(length) >= observed_start:
                if int(length) <= observed_end:
                    cnt += plotdata[str(monday)][length]
                else:
                    over += plotdata[str(monday)][length]

for length in averaged_before:
    if int(length) >= observed_start and int(length) <= observed_end:
        avg_before += averaged_before[length]*int(length)
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
            if int(length) >= observed_start:
                if int(length) <= observed_end:
                    cnt += plotdata[str(monday)][length]
                else:
                    over += plotdata[str(monday)][length]

for length in averaged_after:
    if int(length) >= observed_start and int(length) <= observed_end:
        avg_after += averaged_after[length]*int(length)
avg_after /= cnt
longer_after = 100*over/(cnt+over)

logging.info("Creating plot ...")

fig, ax = plt.subplots()
width = 0.35



values = []
indices = []
cnt_streaks = 0

for length in averaged_before:
    if int(length) >= observed_start and int(length) <= observed_end:
        cnt_streaks += averaged_before[length]


i = observed_start
while i <= observed_end:
    if str(i) in averaged_before:
        for el in bins:
            if i >= el[0] and i <= el[1]:
                binval[bins.index(el)] += averaged_before[str(i)]
    i += 1

i = 1
while i <= len(bins):
    indices.append(i - width/2)
    values.append(binval[i-1]/cnt_streaks)
    i += 1
p1 = ax.bar(indices, values, width, align='center', color="#17719B")



binval = [0, 0, 0, 0]
values = []
indices = []
cnt_streaks = 0

for length in averaged_after:
    if int(length) >= observed_start and int(length) <= observed_end:
        cnt_streaks += averaged_after[length]


i = observed_start
while i <= observed_end:
    if str(i) in averaged_after:
        for el in bins:
            if i >= el[0] and i <= el[1]:
                binval[bins.index(el)] += averaged_after[str(i)]
    i += 1

i = 1
while i <= len(bins):
    indices.append(i + width/2)
    values.append(binval[i-1]/cnt_streaks)
    i += 1
p2 = ax.bar(indices, values, width, align='center', color="#32A875")


ax.set_xticks([1,2,3,4])
ax.set_xticklabels(["15 - 34", "35 - 54", "55 - 74", "75 - 100"])
ax.legend((p1[0], p2[0]), ("Before (avg)", "After (avg)"))
plt.ylabel("Share of streaks with length > 14", fontsize=12)
plt.xlabel("Streak length in days\nBefore: Avg streak length: " + str(round(avg_before, 2)) + "    Streaks longer than 100:  " + str(round(longer_before, 2))+ "%" + 
            "\nAfter: Avg streak length:  " + str(round(avg_after, 2)) + "    Streaks longer than 100:  " + str(round(longer_after, 2)) + "%")
plt.annotate("Nearly no streaks with length >54 \nafter the design change", xy=(3.2,0.07), xytext=(2.4,0.25), arrowprops=dict(facecolor='black', shrink=0.03))
plt.show()


logging.info("Done.")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))
