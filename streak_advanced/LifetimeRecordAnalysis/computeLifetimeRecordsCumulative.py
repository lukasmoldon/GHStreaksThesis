# ---------- IMPORT ------------
import logging
import datetime
import json
from datetime import timedelta, date
# ------------------------------


# ---------- INPUT -------------
path_source_streakdata = "/home/lmoldon/data/user_streaks.json"
path_source_userdata = "/home/lmoldon/data/users_reduced.json"
path_source_genderdata = "/home/lmoldon/data/users_gender.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results_before = "/home/lmoldon/results/lifetimeRecordsPlotBEFORE.json"
path_results_after = "/home/lmoldon/results/lifetimeRecordsPlotAFTER.json"
# ------------------------------


# ---------- CONFIG ------------
minlen = 20
gender = "female" # "" for no gender restriction
country = "" # "" for no country restriction
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
changedate = date(2016, 5, 19)
cnt_streaks_total = 0
cnt_users_before = 0
cnt_users_after = 0
plotdata_before = {}
plotdata_after = {}
# ------------------------------



log_starttime = datetime.datetime.now()

logging.info("Loading data ...")
with open(path_source_streakdata, "r") as fp:
    streakdata = json.load(fp)

with open(path_source_userdata, "r") as fp:
    userids = json.load(fp)

if gender != "":
    with open(path_source_genderdata, "r") as fp:
        genderdata = json.load(fp)
logging.info("Done (1/3)")


deleteIDs = set()
for userid in userids:
    if userid not in streakdata:
        deleteIDs.add(userid)
    elif gender and userid not in genderdata:
        deleteIDs.add(userid)
    elif country and userid not in genderdata:
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

        if length >= minlen:
            if start < changedate and start > date(2013, 1, 1) and user_record_length_before < length:
                user_record_length_before = length
            elif start > changedate and user_record_length_after < length:
                user_record_length_after = length


    if user_record_length_before != -1:
        cnt_users_before += 1
        i = minlen
        while i <= user_record_length_before:
            if str(i) in plotdata_before:
                plotdata_before[str(i)] += 1
            else:
                plotdata_before[str(i)] = 1
            i += 1
    
    if user_record_length_after != -1:
        cnt_users_after += 1
        i = minlen
        while i <= user_record_length_after:
            if str(i) in plotdata_after:
                plotdata_after[str(i)] += 1
            else:
                plotdata_after[str(i)] = 1
            i += 1



for key in plotdata_before:
    plotdata_before[key] = plotdata_before[key] / cnt_users_before

for key in plotdata_after:
    plotdata_after[key] = plotdata_after[key] / cnt_users_after


logging.info("Done. (2/3)")



logging.info("Saving results ...")
with open(path_results_before, "w") as fp:
    json.dump(plotdata_before, fp)
with open(path_results_after, "w") as fp:
    json.dump(plotdata_after, fp)
logging.info("Done. (3/3)")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))