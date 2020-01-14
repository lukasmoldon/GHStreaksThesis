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
path_results_before = "/home/lmoldon/results/lifetimeRecordsBEFORE.json"
path_results_after = "/home/lmoldon/results/lifetimeRecordsAFTER.json"
# ------------------------------


# ---------- CONFIG ------------
bins = [
    [20,39],
    [40,59],
    [60,79],
    [80,99],
    [100,9999999]
]

binvals_before = {
    20: 0,
    40: 0,
    60: 0,
    80: 0,
    100: 0
}

binvals_after = {
    20: 0,
    40: 0,
    60: 0,
    80: 0,
    100: 0
}
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
changedate = date(2016, 5, 19)
cnt_streaks_total = 0
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

    user_record_length_before = -1
    user_record_length_after = -1

    for streakid in streakdata[userid]:  # for each streak of that user
        
        start = datetime.datetime.strptime(str(streakdata[userid][streakid]["start"]), datetimeFormat).date()
        end = datetime.datetime.strptime(str(streakdata[userid][streakid]["end"]), datetimeFormat).date()
        length = int(streakdata[userid][streakid]["len"])

        cnt_streaks_total += 1
        if cnt_streaks_total % 1000000 == 0:
            logging.info(str(cnt_streaks_total/1000000) + " million streaks computed.")

        if length >= bins[0][0]:
            if start < changedate and start > date(2013, 1, 1) and user_record_length_before < length:
                user_record_length_before = length
            elif start > changedate and user_record_length_after < length:
                user_record_length_after = length


    if user_record_length_before != -1:
        for binborder in bins:
            if user_record_length_before >= binborder[0] and user_record_length_before <= binborder[1]:
                binvals_before[binborder[0]] += 1
    
    if user_record_length_after != -1:
        for binborder in bins:
            if user_record_length_after >= binborder[0] and user_record_length_after <= binborder[1]:
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