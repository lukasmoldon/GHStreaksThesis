# ---------- IMPORT ------------
import logging
import matplotlib
import matplotlib.pyplot as plt
import datetime
import json
#import ijson
#from datetime import timedelta, date
# ------------------------------


# ---------- INPUT -------------
path_source_before = "C:/Users/Lukas/Desktop/oneCommitPerDayBehav/streakOneContributionDaysShareMIN60BIN4BEFORE.json"
path_source_after = "C:/Users/Lukas/Desktop/oneCommitPerDayBehav/streakOneContributionDaysShareMIN60BIN4AFTER.json"
# ------------------------------


# ---------- OUTPUT ------------
# ------------------------------


# ---------- CONFIG ------------
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
#datetimeFormat = "%Y-%m-%d"
# ------------------------------


log_starttime = datetime.datetime.now()


logging.info("Accessing plotdata ...")
with open(path_source_before, "r") as fp:
    plotdata_before = json.load(fp)
with open(path_source_after, "r") as fp:
    plotdata_after = json.load(fp)


logging.info("Creating plot ...")

fig, ax = plt.subplots()
width = 0.35


values = []
indices = []

i = 0
while i < len(plotdata_before):
    indices.append(i - width/2)
    values.append(plotdata_before[str(i)])
    i += 1

p1 = ax.bar(indices, values, width, align='center')




values = []
indices = []

i = 0
while i < len(plotdata_after):
    indices.append(i + width/2)
    values.append(plotdata_after[str(i)])
    i += 1


p2 = ax.bar(indices, values, width, align='center')

axes = plt.gca()
axes.set_ylim([0.25,0.45])
ax.set_xticks([0,1,2,3])
ax.set_xticklabels(["0%-25%", "25%-50%", "50%-75%", "75%-100%"])
plt.axhline(y=0.25, c="r")
ax.legend((p1[0], p2[0]), ("Year before the change", "Year after the change"))
plt.ylabel("Share of 1 contribution days over all streaks with length > 30")
plt.xlabel("Streaks lifetime")
#plt.annotate("TEXT", xy=(3.1,0.07), xytext=(2.6,0.2), arrowprops=dict(facecolor='black', shrink=0.03))
plt.show()


logging.info("Done.")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))
