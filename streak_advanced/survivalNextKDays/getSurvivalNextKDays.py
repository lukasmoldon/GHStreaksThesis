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
path_results = "/home/lmoldon/results/nextKDays.json"
# ------------------------------


# ---------- CONFIG ------------
k = 15
bins = [
    [20,29],
    [30,39],
    [40,49],
    [50,59],
    [60,69],
    [70,79],
    [80,89],
    [90,99],
    [100,9999999]
]

observed_mondays = [date(2016, 1, 11), date(2016, 1, 18), date(2016, 1, 25), date(2016, 2, 1), date(
    2016, 2, 8), date(2016, 8, 28), date(2016, 9, 5), date(2016, 9, 12), date(2016, 9, 19), date(2016, 9, 26)]
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
changedate = date(2016, 5, 19)
cnt_streaks_total = 0
plotdata = {}
# ------------------------------



log_starttime = datetime.datetime.now()

for day in observed_mondays:
    plotdata[str(day)] = {}
    for binborder in bins:
        plotdata[str(day)][binborder[0]] = {
            "s": 0, # survived
            "a": 0 # abandoned
        }

logging.info("Loading data ...")
with open(path_source_streakdata, "r") as fp:
    streakdata = json.load(fp)

with open(path_source_userdata, "r") as fp:
    userids = json.load(fp)

logging.info("Done (1/3)")


deleteIDs = set()
for userid in userids:
    if userid not in streakdata:
        deleteIDs.add(userid)

for userid in deleteIDs:
    del userids[userid]


for userid in userids:
    for streakid in streakdata[userid]:

        start = datetime.datetime.strptime(str(streakdata[userid][streakid]["start"]), datetimeFormat).date()
        end = datetime.datetime.strptime(str(streakdata[userid][streakid]["end"]), datetimeFormat).date()
        length = int(streakdata[userid][streakid]["len"])

        cnt_streaks_total += 1
        if cnt_streaks_total % 1000000 == 0:
            logging.info(str(cnt_streaks_total/1000000) + " million streaks computed.")

        for day in observed_mondays:
            if start <= day and end >= day: # monday is part of the streak
                for binborder in bins:
                    if length >= binborder[0] and length <= binborder[1]:
                        if end < (day + datetime.timedelta(days=k)): # streak did not survived to delta + k
                            plotdata[str(day)][binborder[0]]["a"] += 1
                        else: # streak survived
                            plotdata[str(day)][binborder[0]]["s"] += 1



logging.info("Saving results ...")
with open(path_results, "w") as fp:
    json.dump(plotdata, fp)
logging.info("Done. (3/3)")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))