# ---------- IMPORT ------------
import logging
import datetime
import json
from datetime import date, timedelta
# ------------------------------


# ---------- INPUT -------------
path_source = "/home/lmoldon/data/contribution_per_user_per_day.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/results/weekendActivity.json"
# ------------------------------


# ---------- CONFIG ------------
observed_start = date(2016, 1, 4) # this must be a monday
observed_end = date(2017, 1, 1) # this must be a sunday
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
weekdata = {}
# ------------------------------



def getWeekMonday(strdate):
    date = datetime.datetime.strptime(date, datetimeFormat).date()
    monday = date - timedelta(days=date.weekday())
    if monday >= observed_start and monday <= observed_end:
        return monday
    else:
        return -1 # out of observed range (not in weekdata)

def isWeekend(strdate):
    date = datetime.datetime.strptime(date, datetimeFormat).date()
    if date.weekday() < 5:
        return False
    else:
        return True


log_starttime = datetime.datetime.now()

logging.info("Loading data ...")
with open(path_source, "r") as fp:
    contributiondata = json.load(fp)
logging.info("Done (1/3)")


logging.info("Starting ...")

i = observed_start
while i < observed_end:
    weekdata[str(i)] = {"WD": 0, "WE": 0, "RW:": 0} # RW: ratio weekend activity
    i += timedelta(days=7)

for userID in contributiondata:
    for day in contributiondata[userID]:
        monday = getWeekMonday(day)
        if monday != -1:
            if not isWeekend(day):
                weekdata[str(monday)]["WD"] += 1
            else:
                weekdata[str(monday)]["WE"] += 1

for index in weekdata:
    weekdata[index]["RW"] = weekdata[index]["WE"] / (weekdata[index]["WD"] + weekdata[index]["WE"])

logging.info("Done (2/3)")


logging.info("Saving results ...")
with open(path_results, "w") as fp:
    json.dump(weekdata, fp)
logging.info("Done. (3/3)")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))