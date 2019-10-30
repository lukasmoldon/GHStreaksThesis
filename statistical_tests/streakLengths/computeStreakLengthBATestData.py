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
path_source_streakdata = "/home/lmoldon/data/user_streaks.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results_before = "/home/lmoldon/results/streakLengthsBefore.json"
path_results_after = "/home/lmoldon/results/streakLengthsAfter.json"
# ------------------------------


# ---------- CONFIG ------------
interval = 21 # days before and after the design change which get observed
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
data_before = []
data_after = []
removaldate = date(2016, 5, 19)
observed_start = removaldate - datetime.timedelta(days=interval)
observed_end = removaldate + datetime.timedelta(days=interval)
cnt_streaks = 0
cnt_streaks_before = 0
cnt_streaks_after = 0
# ------------------------------


log_starttime = datetime.datetime.now()


logging.info("Computing test datasets ...")

streakdata = ijson.parse(open(path_source_streakdata, "r"))
for prefix, event, value in streakdata:
    if ".start" in prefix:
        start = datetime.datetime.strptime(str(value), datetimeFormat).date()
        cnt_streaks += 1
        if cnt_streaks % 1000000 == 0:
            logging.info(str(cnt_streaks/1000000) +
                         " million streaks computed.")
    elif ".end" in prefix:
        # end = datetime.datetime.strptime(str(value), datetimeFormat).date()
        pass
    elif ".len" in prefix:
        if start >= observed_start and start < removaldate:
            data_before.append(int(value))
            cnt_streaks_before += 1
        elif start > removaldate and start <= observed_end:
            data_after.append(int(value))
            cnt_streaks_after += 1

logging.info("Done. (1/2)")



logging.info("Saving datasets ...")

with open(path_results_after, "w") as fp:
    json.dump(data_after, fp)

with open(path_results_before, "w") as fp:
    json.dump(data_before, fp)


logging.info("Done. (2/2)")

logging.info("Streaks before: " + str(cnt_streaks_before))
logging.info("Streaks after: " + str(cnt_streaks_after))

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))
