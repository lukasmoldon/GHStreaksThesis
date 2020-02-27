# ---------- IMPORT ------------
import logging
import datetime
import json
from datetime import date, timedelta
import matplotlib
#import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
# ------------------------------


# ---------- INPUT -------------
path_source_before = "C:/Users/Lukas/Desktop/zscoresBEFORE.json"
path_source_after = "C:/Users/Lukas/Desktop/zscoresAFTER.json"
# ------------------------------


# ---------- OUTPUT ------------
# ------------------------------


# ---------- CONFIG ------------

# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
before = []
after = []
# ------------------------------



log_starttime = datetime.datetime.now()

with open(path_source_before, "r") as fp:
    plotdata_before = json.load(fp)

with open(path_source_after, "r") as fp:
    plotdata_after = json.load(fp)

max_before = 0
cnt_before = 0
for userid in plotdata_before:
    before.append(plotdata_before[userid])
    if plotdata_before[userid] > 50:
        cnt_before += 1
    max_before = max(plotdata_before[userid], max_before)

max_after = 0
cnt_after = 0
for userid in plotdata_after:
    after.append(plotdata_after[userid])
    if plotdata_after[userid] > 50:
        cnt_after += 1
    max_after = max(plotdata_after[userid], max_after)

#sns.distplot(before, bins=10, kde=True, rug=True)
#sns.distplot(after, bins=10, kde=True, rug=True)

plt.hist(before, bins=500, density=True, range=(-10,50), color="#1F77B4", label="Before")
plt.axvline(x=np.mean(before), color='k', label="Mean before = " + str(round(np.mean(before), 2)))

plt.hist(after, bins=500, density=True, range=(-10,50), color="#FF7F0E", label="After")
plt.axvline(x=np.mean(after), color='k', label="Mean after = " + str(round(np.mean(after), 2)))

plt.xlabel("z score distribution", fontsize=12)
plt.ylabel("%", fontsize=12)
plt.axvline(x=1.96, color='r', label="x = 1.96")

plt.legend()
#plt.show()


logging.info("Share BEFORE: " + str(100*cnt_before/len(before)))
logging.info("Share AFTER: " + str(100*cnt_after/len(after)))
logging.info("max BEFORE: " + str(max_before))
logging.info("max AFTER: " + str(max_after))

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))