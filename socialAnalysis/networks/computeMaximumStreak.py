# ---------- IMPORT ------------
import logging
import datetime
from datetime import date
import json
# ------------------------------


# ---------- INPUT -------------
path_source_streakdata = "/home/lmoldon/data/user_streaks.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/data/maximumStreak.json"
# ------------------------------


# ---------- CONFIG ------------

# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
maximumStreaks = {}
changedate = date(2016, 5, 19)
# ------------------------------



log_starttime = datetime.datetime.now()


logging.info("Loading data ...")
with open(path_source_streakdata, "r") as fp:
    streakdata = json.load(fp)
logging.info("Done (1/3)")


logging.info("Starting ... ")

cnt_streaks_total = 0

for userid in streakdata:

    maxStreak = 1

    for streakid in streakdata[userid]:  # for each streak of that user
        
        start = datetime.datetime.strptime(str(streakdata[userid][streakid]["start"]), datetimeFormat).date()
        end = datetime.datetime.strptime(str(streakdata[userid][streakid]["end"]), datetimeFormat).date()
        length = int(streakdata[userid][streakid]["len"])

        cnt_streaks_total += 1
        if cnt_streaks_total % 1000000 == 0:
            logging.info(str(cnt_streaks_total/1000000) + " million streaks computed.")

        if length > maxStreak and start < changedate:
            maxStreak = length

    if maxStreak > 1:
        maximumStreaks[str(userid)] = maxStreak

logging.info("Done (2/3)")


logging.info("Saving results ...")
with open(path_results, "w") as fp:
    json.dump(maximumStreaks, fp)
logging.info("Done. (3/3)")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))