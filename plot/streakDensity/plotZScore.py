# ---------- IMPORT ------------
import logging
import datetime
import json
from datetime import date, timedelta
import matplotlib
#import seaborn as sns
import matplotlib.pyplot as plt
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


for userid in plotdata_before:
    before.append(plotdata_before[userid])

for userid in plotdata_after:
    after.append(plotdata_after[userid])

#sns.distplot(before, bins=10, kde=True, rug=True)
#sns.distplot(after, bins=10, kde=True, rug=True)

plt.hist(before, bins=500, density=True, range=(-10,50))
plt.xlabel("z score distribution year before the change")
plt.ylabel("%")
plt.axvline(x=2, color='r', label="x = 2")
plt.legend()
plt.show()

plt.hist(after, bins=500, density=True, range=(-10,50))
plt.xlabel("z score distribution year after the change")
plt.ylabel("%")
plt.axvline(x=2, color='r', label="x = 2")
plt.legend()
plt.show()

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))