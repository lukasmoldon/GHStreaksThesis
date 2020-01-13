# ---------- IMPORT ------------
import logging
import datetime
import json
from datetime import timedelta, date
# ------------------------------


# ---------- INPUT -------------
path_source_streakdata = "/home/lmoldon/data/user_streaks.json"
path_source_userdata = "/home/lmoldon/data/users_reduced.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results_before = "/home/lmoldon/results/streakLengthDistributionBEFORE.json"
path_results_after = "/home/lmoldon/results/streakLengthDistributionAFTER.json"
# ------------------------------


# ---------- CONFIG ------------
offset = 20 # on changedate for BEFORE case
minlen = 20
observed_start = date(2013, 1, 1)
observed_end = date(2019, 4, 1)
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
changedate = date(2016, 5, 19)
distribution_before = {}
distribution_after = {}
# ------------------------------



log_starttime = datetime.datetime.now()

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


logging.info("Starting ...")

for userid in userids:  # for each user in subpopulation
    for streakid in streakdata[userid]:  # for each streak of that user
        
        start = datetime.datetime.strptime(str(streakdata[userid][streakid]["start"]), datetimeFormat).date()
        end = datetime.datetime.strptime(str(streakdata[userid][streakid]["end"]), datetimeFormat).date()
        length = int(streakdata[userid][streakid]["len"])

        cnt_streaks_total += 1
        if cnt_streaks_total % 1000000 == 0:
            logging.info(str(cnt_streaks_total/1000000) + " million streaks computed.")

        if length >= minlen:
            if start < changedate and end <= (changedate + timedelta(days=offset)):
                if length in distribution_before:
                    distribution_before[length] += 1
                else:
                    distribution_before[length] = 1
            elif start > changedate:
                if length in distribution_before:
                    distribution_after[length] += 1
                else:
                    distribution_after[length] = 1



logging.info("Done. (2/3)")


logging.info("Saving results ...")
with open(path_results_before, "w") as fp:
    json.dump(distribution_before, fp)
with open(path_results_after, "w") as fp:
    json.dump(distribution_after, fp)
logging.info("Done. (3/3)")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))