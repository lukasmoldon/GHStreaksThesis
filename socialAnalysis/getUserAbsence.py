# ---------- IMPORT ------------
import logging
import datetime
import json
from datetime import date, timedelta
# ------------------------------


# ---------- INPUT -------------
path_source_contributions = "/home/lmoldon/data/contributions_per_user_per_day.json"
path_source_users = "/home/lmoldon/data/users_reduced.json"
path_source_groupsize = "/home/lmoldon/data/usergroupsize.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "..."
# ------------------------------


# ---------- CONFIG ------------
observed_start = date(2011, 1, 1)
observed_end = date(2019, 4, 1)
minDaysOffline = 1 # how many offline days in a row to be counted?
restriction = False
usertype_restriction = "/home/lmoldon/results/identifyStreakers/nonStreakingUsersMAX5.json"
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
resultdata = {}
path_results = "/home/lmoldon/results/userAbsenceMIN" + str(minDaysOffline) + ".json"
# ------------------------------



def daterange(observedtime_start, observedtime_end):
        for n in range(int((observedtime_end - observedtime_start).days + 1)):
                yield observedtime_start + timedelta(n)

log_starttime = datetime.datetime.now()

logging.info("Loading data ...")
with open(path_source_contributions, "r") as fp:
    contributiondata = json.load(fp)
with open(path_source_users, "r") as fp:
    userdata = json.load(fp)
with open(path_source_groupsize, "r") as fp:
    groupsize = json.load(fp)
logging.info("Done (1/3)")


logging.info("Starting ...")


if restriction:
    with open(usertype_restriction, "r") as fp:
        restrictionIDs = json.load(fp)

    delIDs = set()
    for userID in contributiondata:
        if userID not in restrictionIDs:
            delIDs.add(userID)
    for userID in delIDs:
        del contributiondata[userID]

    groupsize = {}
    for day in daterange(observed_start, observed_end):
        groupsize[str(day)] = 0

    for userID in restrictionIDs:

        created = datetime.datetime.strptime(userdata[userID]["created_at"], "%Y-%m-%d %H:%M:%S").date()
        if created < observed_end:
            if observed_start < created:
                start = created
            else:
                start = observed_start

            for day in daterange(start, observed_end):
                groupsize[str(day)] += 1


for day in daterange(observed_start, observed_end):
    resultdata[str(day)] = 0

cnt_users_total = 0

for userID in contributiondata:

    cnt_users_total += 1
    if cnt_users_total % 10000 == 0:
        logging.info(str(cnt_users_total/1000) + "k users computed.")

    created = datetime.datetime.strptime(userdata[userID]["created_at"], "%Y-%m-%d %H:%M:%S").date()
    if observed_start < created:
        start = created
    else:
        start = observed_start


    withinOffline = False
    cur_OfflineLength = 0
    cur_OfflineStart = None

    for day in daterange(start, observed_end):

        if not withinOffline:
            if str(day) not in contributiondata[userID]:
                withinOffline = True
                cur_OfflineLength = 1
                cur_OfflineStart = day
        else:
            if str(day) not in contributiondata[userID]:
                cur_OfflineLength += 1
            else:
                if cur_OfflineLength >= minDaysOffline:
                    for offlineDay in daterange(cur_OfflineStart, day - timedelta(days=1)):
                        resultdata[str(offlineDay)] += 1
                withinOffline = False
                cur_OfflineLength = 0
                cur_OfflineStart = None
            
    if cur_OfflineLength >= minDaysOffline:
        for offlineDay in daterange(cur_OfflineStart, day - timedelta(days=1)):
            resultdata[str(offlineDay)] += 1


for day in daterange(observed_start, observed_end):
    resultdata[str(day)] = resultdata[str(day)]/groupsize[str(day)]


logging.info("Done (2/3)")


logging.info("Saving results ...")
with open(path_results, "w") as fp:
    json.dump(resultdata, fp)
logging.info("Done. (3/3)")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))