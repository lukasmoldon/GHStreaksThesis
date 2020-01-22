# ---------- IMPORT ------------
import logging
import datetime
import json
# ------------------------------


# ---------- INPUT -------------
path_source_streakdata = "/home/lmoldon/data/user_streaks.json"
path_source_userdata = "/home/lmoldon/data/users_reduced.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "..."
# ------------------------------


# ---------- CONFIG ------------
minlen = 32
before = False
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
quit_ids = {}

if before:
    path_results = "/home/lmoldon/results/quittingUsersMIN" + str(minlen) + "BEFORE.json"
    observed_start = datetime.date(2016, 2, 18)
    observed_end = datetime.date(2016, 2, 27)
else:
    path_results = "/home/lmoldon/results/quittingUsersMIN" + str(minlen) + "AFTER.json"
    observed_start = datetime.date(2016, 5, 19)
    observed_end = datetime.date(2016, 5, 28)
# ------------------------------



log_starttime = datetime.datetime.now()


logging.info("Loading data ...")
with open(path_source_streakdata, "r") as fp:
    streakdata = json.load(fp)

with open(path_source_userdata, "r") as fp:
    userids = json.load(fp)

logging.info("Done (1/3)")


logging.info("Starting...")
cnt_streaks_total = 0

for userid in streakdata:  # for each user
    
    for streakid in streakdata[userid]:  # for each streak of that user

        start = datetime.datetime.strptime(str(streakdata[userid][streakid]["start"]), datetimeFormat).date()
        end = datetime.datetime.strptime(str(streakdata[userid][streakid]["end"]), datetimeFormat).date()
        length = int(streakdata[userid][streakid]["len"])

        cnt_streaks_total += 1
        if cnt_streaks_total % 1000000 == 0:
            logging.info(str(cnt_streaks_total/1000000) + " million streaks computed.")

        if end >= observed_start and end <= observed_end and length >= minlen: # streak >= minlen ended in observed time
            quit_ids[userid] = length



logging.info("Done. (2/3)")


logging.info("Saving results ...")
with open(path_results, "w") as fp:
    json.dump(quit_ids, fp)
logging.info("Done. (3/3)")

logging.info("Total number of quitting users: " + str(len(quit_ids)))

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))