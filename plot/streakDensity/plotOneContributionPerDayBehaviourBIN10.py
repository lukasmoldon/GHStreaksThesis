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
path_source_before = "C:/Users/Lukas/Desktop/oneCommitPerDayBehav/streakOneContributionDaysBEFORE_BIN10_MIN30.json"
path_source_after = "C:/Users/Lukas/Desktop/oneCommitPerDayBehav/streakOneContributionDaysAFTER_BIN10_MIN30.json"
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
axes.set_ylim([0.076,0.135])
ax.set_xticks([0,1,2,3,4,5,6,7,8,9])
ax.set_xticklabels(["0%-10%", "10%-20%", "20%-30%", "30%-40%", "40%-50%", "50%-60%", "60%-70%", "70%-80%", "80%-90%", "90%-100%"])
plt.axhline(y=0.1, c="r")
ax.legend((p1[0], p2[0]), ("Year before the change", "Year after the change"))
plt.ylabel("Distribution of 1 contribution days over all streaks with length > 30")
plt.xlabel("Streaks lifetime")
#plt.annotate("TEXT", xy=(3.1,0.07), xytext=(2.6,0.2), arrowprops=dict(facecolor='black', shrink=0.03))
plt.show()


logging.info("Done.")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))
