# ---------- IMPORT ------------
import logging
import json
import datetime
import numpy as np
from scipy.stats import ks_2samp
from datetime import timedelta, date
# ------------------------------


# ---------- INPUT -------------
path_source_before = "..."
path_source_after = "..."
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
week = 5 # [1,5] - calendar week in 2016/17
observed_mondays = [date(2016, 1, 11), date(2016, 1, 18), date(2016, 1, 25), date(2016, 2, 1), date(
    2016, 2, 8), date(2017, 1, 9), date(2017, 1, 16), date(2017, 1, 23), date(2017, 1, 30), date(
    2017, 2, 6)]
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
data_before = []
data_after = []
path_source_before = "/home/lmoldon/results/streakLengthsKSMondayBeforeWEEK" + str(week) + ".json"
path_source_after = "/home/lmoldon/results/streakLengthsKSMondayAfterWEEK" + str(week) + ".json"
# ------------------------------



log_starttime = datetime.datetime.now()

logging.info("Loading data ...")
with open(path_source_before, "r") as fp:
    distribution_before = json.load(fp)

with open(path_source_after, "r") as fp:
    distribution_after = json.load(fp)

logging.info("Done (1/2)")


tmp = []
tmp.append(observed_mondays[week-1])
tmp.append(observed_mondays[int((len(observed_mondays)/2)-1+week)])
observed_mondays = tmp
observed_mondays = tmp
logging.info("Selected the follwing Mondays:" + str(observed_mondays[0]) + "  and   " + str(observed_mondays[1]))


logging.info("Result:")
print(ks_2samp(distribution_before,distribution_after))



log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))