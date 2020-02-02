# ---------- IMPORT ------------
import logging
import datetime
import json
from datetime import date, timedelta
# ------------------------------


# ---------- INPUT -------------
path_source_streakdata = "/home/lmoldon/data/user_streaks.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/results/weekendStreaks.json"
# ------------------------------


# ---------- CONFIG ------------
minlen = 12
observed_start = date(2016, 1, 4) # this must be a monday
observed_end = date(2017, 1, 1) # this must be a sunday
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
changedate = date(2016, 5, 19)
cnt_streaks_total = 0
weekdata = {}
path_results = "/home/lmoldon/results/weekendStreaksMIN" + str(minlen) + ".json"
# ------------------------------



def getWeekMonday(strdate):
    date = datetime.datetime.strptime(strdate, datetimeFormat).date()
    monday = date - timedelta(days=date.weekday())
    if monday >= observed_start and monday <= observed_end:
        return monday
    else:
        return -1 # out of observed range (not in weekdata)

def isWeekend(strdate):
    date = datetime.datetime.strptime(strdate, datetimeFormat).date()
    if date.weekday() < 5:
        return False
    else:
        return True


log_starttime = datetime.datetime.now()

logging.info("Loading data ...")
with open(path_source_streakdata, "r") as fp:
    streakdata = json.load(fp)
logging.info("Done (1/3)")


logging.info("Starting ...")

i = observed_start
while i < observed_end:
    weekdata[str(i)] = {"WD": 0, "WE": 0, "RW:": 0} # RW: ratio streaks ending on the weekend
    i += timedelta(days=7)

for userid in streakdata:
    for streakid in streakdata[userid]:

        start = datetime.datetime.strptime(str(streakdata[userid][streakid]["start"]), datetimeFormat).date()
        end = datetime.datetime.strptime(str(streakdata[userid][streakid]["end"]), datetimeFormat).date()
        length = int(streakdata[userid][streakid]["len"])

        cnt_streaks_total += 1
        if cnt_streaks_total % 1000000 == 0:
            logging.info(str(cnt_streaks_total/1000000) + " million streaks computed.")

        if end >= observed_start and end <= observed_end and length >= minlen:
            monday = getWeekMonday(str(end))
            if monday != -1:
                if not isWeekend(str(end)):
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