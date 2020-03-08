# ---------- IMPORT ------------
import logging
import datetime
import json
from datetime import date, timedelta
# ------------------------------


# ---------- INPUT -------------
path_source = "/home/lmoldon/data/contributions_per_user_per_day.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "..."
# ------------------------------


# ---------- CONFIG ------------
observed_start = date(2016, 1, 4) # this must be a monday
observed_end = date(2016, 12, 31) # this must be a sunday
min_active_start = date(2016, 5, 19)
min_active_end = date(2016, 4, 18)
userlevel = True # True: datapoint represents single user per day, False: represents avg of all users per day
minTotalActivity = 30 # minimum number of contributions in full observed time to be counted (ONLY FOR USERLEVEL = TRUE)
minWeekActivity = 1 # minimum number of contributions in a specifc week to be counted in that week (ONLY FOR USERLEVEL = TRUE)
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
weekdata = {}
cnt_users_total = 0
if userlevel:
    path_results = "/home/lmoldon/results/weekendActivity_userlevel_reconstruct.json"
else:
    path_results = "/home/lmoldon/results/weekendActivity.json"
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
with open(path_source, "r") as fp:
    contributiondata = json.load(fp)
logging.info("Done (1/3)")


logging.info("Starting ...")

if not userlevel:
    i = observed_start
    while i < observed_end:
        weekdata[str(i)] = {"WD": 0, "WE": 0, "RW:": 0} # RW: ratio weekend activity
        i += timedelta(days=7)

    for userID in contributiondata:

        cnt_users_total += 1
        if cnt_users_total % 10000 == 0:
            logging.info(str(cnt_users_total/1000) + "k users computed.")

        for day in contributiondata[userID]:
            monday = getWeekMonday(day)
            if monday != -1:
                if not isWeekend(day):
                    weekdata[str(monday)]["WD"] += contributiondata[userID][day]
                else:
                    weekdata[str(monday)]["WE"] += contributiondata[userID][day]

    for index in weekdata:
        weekdata[index]["RW"] = weekdata[index]["WE"] / (weekdata[index]["WD"] + weekdata[index]["WE"])
else:
    i = observed_start
    while i < observed_end:
        weekdata[str(i)] = {}
        for userID in contributiondata:
            weekdata[str(i)][userID] = {"WD": 0, "WE": 0, "RW:": 0} # RW: ratio weekend activity
        i += timedelta(days=7)

    for userID in contributiondata:

        cnt_users_total += 1
        if cnt_users_total % 10000 == 0:
            logging.info(str(cnt_users_total/1000) + "k users computed.")

        for day in contributiondata[userID]:
            monday = getWeekMonday(day)
            if monday != -1:
                if not isWeekend(day):
                    weekdata[str(monday)][userID]["WD"] += contributiondata[userID][day]
                else:
                    weekdata[str(monday)][userID]["WE"] += contributiondata[userID][day]

    for userID in contributiondata:
        activity = 0
        for index in weekdata:
            d = datetime.datetime.strptime(index, datetimeFormat).date()
            if (weekdata[index][userID]["WD"] + weekdata[index][userID]["WE"]) >= minWeekActivity:
                weekdata[index][userID]["RW"] = weekdata[index][userID]["WE"] / (weekdata[index][userID]["WD"] + weekdata[index][userID]["WE"])
                if d < min_active_start and d >= min_active_end:
                    activity += (weekdata[index][userID]["WD"] + weekdata[index][userID]["WE"])
            else:
                del weekdata[index][userID]
        if activity < minTotalActivity:
            for index in weekdata:
                if userID in weekdata[index]:
                    del weekdata[index][userID]

logging.info("Done (2/3)")


logging.info("Saving results ...")
with open(path_results, "w") as fp:
    json.dump(weekdata, fp)
logging.info("Done. (3/3)")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))