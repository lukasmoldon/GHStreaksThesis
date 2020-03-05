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
# IMPORTANT! TOTAL values get stored!
path_results_values = "/home/lmoldon/results/mondayLongStreakValues.json"
# ------------------------------


# ---------- CONFIG ------------
observed_startday = 7 # where to start counting lengths? (e.g. 7 = Sunday same week)
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
plotdata = {}
cnt_streaks = 0
observed_mondays = [
    date(2016, 1, 4), 
    date(2016, 1, 11),
    date(2016, 1, 18), 
    date(2016, 1, 25), 
    date(2016, 2, 1), 
    date(2016, 2, 8), 
    date(2016, 2, 15), 
    date(2016, 2, 22), 
    date(2016, 2, 29), 
    date(2016, 3, 7),
    date(2017, 1, 2), 
    date(2017, 1, 9),
    date(2017, 1, 16), 
    date(2017, 1, 23), 
    date(2017, 1, 30), 
    date(2017, 2, 6), 
    date(2017, 2, 13), 
    date(2017, 2, 20), 
    date(2017, 2, 27), 
    date(2017, 3, 6)
    ]
# ------------------------------


log_starttime = datetime.datetime.now()

for monday in observed_mondays:
    plotdata[str(monday)] = {}

logging.info("Starting ...")

streakdata = ijson.parse(open(path_source_streakdata, "r"))
for prefix, event, value in streakdata:
    if ".start" in prefix:
        start = datetime.datetime.strptime(str(value), datetimeFormat).date()
        cnt_streaks += 1
        if cnt_streaks % 1000000 == 0:
            logging.info(str(cnt_streaks/1000000) + " million streaks computed.")
    elif ".end" in prefix:
        end = datetime.datetime.strptime(str(value), datetimeFormat).date()
    elif ".len" in prefix:
        if int(value) >= observed_startday:
            if start in observed_mondays:
                if str(value) in plotdata[str(start)]:
                    plotdata[str(start)][str(value)] += 1
                else:
                    plotdata[str(start)][str(value)] = 1

logging.info("Done. (1/2)")



logging.info("Saving plot data ...")

with open(path_results_values, "w") as fp:
    json.dump(plotdata, fp)


logging.info("Done. (2/2)")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))
