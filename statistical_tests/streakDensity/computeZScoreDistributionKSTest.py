# ---------- IMPORT ------------
import logging
import json
import datetime
import numpy as np
from scipy.stats import ks_2samp
# ------------------------------


# ---------- INPUT -------------
path_source_before = "/home/lmoldon/results/zscoresBEFORE.json"
path_source_after = "/home/lmoldon/results/zscoresAFTER.json"
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

logging.info("Result:")
print(ks_2samp(before, after))

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))