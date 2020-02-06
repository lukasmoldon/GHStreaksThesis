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
path_results_before = "..."
path_results_after = "..."
# ------------------------------


# ---------- CONFIG ------------
k = 12 # minlen
week = 1 # [1,5] - calendar week in 2016/17
observed_mondays = [date(2016, 1, 11), date(2016, 1, 18), date(2016, 1, 25), date(2016, 2, 1), date(
    2016, 2, 8), date(2017, 1, 9), date(2017, 1, 16), date(2017, 1, 23), date(2017, 1, 30), date(
    2017, 2, 6)]
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
data_before = []
data_after = []
removaldate = date(2016, 5, 19)
cnt_streaks = 0
cnt_streaks_before = 0
cnt_streaks_after = 0
path_results_before = "/home/lmoldon/results/streakLengthsKSMondayBeforeWEEK" + str(week) + ".json"
path_results_after = "/home/lmoldon/results/streakLengthsKSMondayAfterWEEK" + str(week) + ".json"
# ------------------------------


log_starttime = datetime.datetime.now()


tmp = []
tmp.append(observed_mondays[week-1])
tmp.append(observed_mondays[int((len(observed_mondays)/2)-1+week)])
observed_mondays = tmp
observed_mondays = tmp
logging.info("Selected the follwing Mondays:" + str(observed_mondays[0]) + "  and   " + str(observed_mondays[1]))


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
        for monday in observed_mondays:
            if start == monday and monday < removaldate and int(value) >= k:
                data_before.append(int(value))
                cnt_streaks_before += 1
            elif start == monday and monday > removaldate and int(value) >= k:
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
