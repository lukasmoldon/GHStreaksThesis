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
path_results_before = "/home/lmoldon/results/streakLengthBINDistributionBEFORE.json"
path_results_after = "/home/lmoldon/results/streakLengthBINDistributionAFTER.json"
# ------------------------------


# ---------- CONFIG ------------
bins = [
    [20,29],
    [30,39],
    [40,49],
    [50,59],
    [60,69],
    [70,79],
    [80,89],
    [90,99],
    [100,199],
    [200,299],
    [300,5000],
]

binvals_before = {
    20: 0,
    30: 0,
    40: 0,
    50: 0,
    60: 0,
    70: 0,
    80: 0,
    90: 0,
    100: 0,
    200: 0,
    300: 0,
}

binvals_after = {
    20: 0,
    30: 0,
    40: 0,
    50: 0,
    60: 0,
    70: 0,
    80: 0,
    90: 0,
    100: 0,
    200: 0,
    300: 0,
}
offset = 20 # on changedate for BEFORE case
observed_start = date(2013, 1, 1)
observed_end = date(2019, 4, 1)
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
changedate = date(2016, 5, 19)
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

        if length >= bins[0][0]:
            for binborder in bins:
                if length >= binborder[0] and length <= binborder[1]:
                    if start < changedate and end <= (changedate + timedelta(days=offset)):
                        binvals_before[binborder[0]] += 1
                    elif start > changedate:
                        binvals_after[binborder[0]] += 1



logging.info("Done. (2/3)")


logging.info("Saving results ...")
with open(path_results_before, "w") as fp:
    json.dump(binvals_before, fp)
with open(path_results_after, "w") as fp:
    json.dump(binvals_after, fp)
logging.info("Done. (3/3)")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))