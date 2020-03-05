# ---------- IMPORT ------------
import logging
import datetime
from datetime import date, timedelta
import json
# ------------------------------


# ---------- INPUT -------------
path_source_streakdata = "/home/lmoldon/data/user_streaks.json"
path_source_userdata = "/home/lmoldon/data/users_reduced.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/results/survivalOverTime.json"
# ------------------------------


# ---------- CONFIG ------------
cut = 500
observed_weeks = [
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


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
cnt_streaks_total = 0
plotdata = {}
# ------------------------------


def getWeekMonday(strdate):
    date = datetime.datetime.strptime(strdate, datetimeFormat).date()
    monday = date - timedelta(days=date.weekday())
    if monday in observed_weeks:
        return monday
    else:
        return -1 # out of observed range (not in weekdata)

log_starttime = datetime.datetime.now()

logging.info("Loading data ...")
with open(path_source_streakdata, "r") as fp:
    streakdata = json.load(fp)

with open(path_source_userdata, "r") as fp:
    userids = json.load(fp)

for week in observed_weeks:
    i = 0
    plotdata[str(week)] = {}
    while i <= cut:
        plotdata[str(week)][str(i)] = 0
        i += 1

logging.info("Done (1/3)")


logging.info("Starting ...")

for userid in streakdata:
    for streakid in streakdata[userid]:

        start = datetime.datetime.strptime(str(streakdata[userid][streakid]["start"]), datetimeFormat).date()
        end = datetime.datetime.strptime(str(streakdata[userid][streakid]["end"]), datetimeFormat).date()
        length = int(streakdata[userid][streakid]["len"])

        cnt_streaks_total += 1
        if cnt_streaks_total % 1000000 == 0:
            logging.info(str(cnt_streaks_total/1000000) + " million streaks computed.")

        week = getWeekMonday(str(start))
        if week != -1:
            i = 1
            while i <= min(length, cut):
                plotdata[str(week)][str(i)] += 1
                i += 1

logging.info("Done (2/3)")


logging.info("Saving results ...")
with open(path_results, "w") as fp:
    json.dump(plotdata, fp)
logging.info("Done. (3/3)")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))