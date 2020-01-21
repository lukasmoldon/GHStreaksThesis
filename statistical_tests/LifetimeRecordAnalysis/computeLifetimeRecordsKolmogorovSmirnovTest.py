# ---------- IMPORT ------------
import logging
import json
import datetime
import numpy as np
from scipy.stats import ks_2samp
# ------------------------------


# ---------- INPUT -------------
path_source_before = "/home/lmoldon/results/lifetimeRecordsDistributionBEFORE.json"
path_source_after = "/home/lmoldon/results/lifetimeRecordsDistributionAFTER.json"
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------

# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
data_before = []
data_after = []
# ------------------------------



log_starttime = datetime.datetime.now()

logging.info("Loading data ...")
with open(path_source_before, "r") as fp:
    distribution_before = json.load(fp)

with open(path_source_after, "r") as fp:
    distribution_after = json.load(fp)

logging.info("Done (1/2)")



logging.info("Starting ...")


for length in distribution_before:
    data_before += (distribution_before[length] * [int(length)])

for length in distribution_after:
    data_after += (distribution_after[length] * [int(length)])


logging.info("Done. (2/2)")



logging.info("Result:")
print(ks_2samp(data_before,data_after))



log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))