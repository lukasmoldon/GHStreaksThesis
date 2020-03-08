# ---------- IMPORT ------------
import logging
import datetime
from datetime import date, timedelta
import json
import numpy as np
import pandas as pd
from rdd import rdd
# ------------------------------


# ---------- INPUT -------------
path_source = "..."
path_source_genderdata = "/home/lmoldon/data/users_gender.json"
path_source_merge = "/home/lmoldon/data/merge.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/results/weekendRDD.json"
# ------------------------------


# ---------- CONFIG ------------
observed_start = date(2016, 1, 4) # this must be a monday and the same input of getWeekendActivity.py
observed_end = date(2016, 12, 31) # this must be a sunday and the same input of getWeekendActivity.py
userlevel = True # True: datapoint represents single user per day, False: represents avg of all users per day
# IMPORTANT: in the paper bandwidth means full observed time interval, here it means bandwidth +/- around cut (2x for bandwidth length)
bandwidth = 2 # maximum: (observed_end - observed_start).weeks() / 2
country = "" # restrict rdd on users from a specific country, if empty - disable feature (ONLY FOR USERLEVEL = TRUE)
gender = "" # restrict rdd on female/male users, if empty streak - feature (ONLY FOR USERLEVEL = TRUE)
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
results = {}
changedates = []
if userlevel:
    path_source = "/home/lmoldon/results/weekendActivity_userlevel.json"
else:
    path_source = "/home/lmoldon/results/weekendActivity.json"
# ------------------------------



def daterange(observedtime_start, observedtime_end):
        for n in range(int((observedtime_end - observedtime_start).days + 1)):
                yield observedtime_start + timedelta(n)



log_starttime = datetime.datetime.now()



logging.info("Loading data ...")

with open(path_source, "r") as fp:
    weekdata = json.load(fp)

with open(path_source_genderdata, "r") as fp:
    genderdata = json.load(fp)

with open(path_source_merge, "r") as fp:
    merge = json.load(fp)

logging.info("Done. (1/4)")



logging.info("Creating model setup ...")

if country != "" or gender != "":
    for userID in genderdata:
        if genderdata[userID]["country"] in merge:
            genderdata[userID]["country"] = merge[genderdata[userID]["country"]]

    delIDs = set()
    for day in daterange(observed_start, observed_end):
        if str(day) in weekdata:
            for userID in weekdata[str(day)]:
                if userID not in genderdata:
                    delIDs.add(userID)

    for userID in delIDs:
        for day in daterange(observed_start, observed_end):
            if str(day) in weekdata:
                if userID in weekdata[str(day)]:
                    del weekdata[str(day)][userID]

for day in daterange(observed_start+timedelta(days=7*(bandwidth+1)), observed_end-timedelta(days=7*(bandwidth+1))):
    if day.weekday() == 0:
        changedates.append(day)
        results[str(day)] = {
            "TREATED": None,
            "p": None,
            "a": None,
            "b": None
        }

logging.info("Done. (2/4)")



logging.info("Computing models ...")

cnt = 0
for changedate in changedates:
    x = []
    y = []
    cnt = 1 # index of current week
    change_cnt = -1 # index of first week after the change = cut
    if not userlevel:
        for day in daterange(observed_start, observed_end):
            if str(day) in weekdata and str(day) != str(changedate):
                x.append(cnt)
                y.append(weekdata[str(day)]["RW"])
                if day > changedate and change_cnt == -1:
                    change_cnt = cnt
                cnt += 1
            if str(day) in weekdata and str(day) == str(changedate):
                change_cnt = cnt
                cnt += 1
    else:
        for day in daterange(observed_start, observed_end):
            if str(day) in weekdata and str(day) != str(changedate):
                for userID in weekdata[str(day)]:
                    if country == "" or genderdata[userID]["country"] == country:
                        if gender == "" or genderdata[userID]["gender"] == gender:
                            x.append(cnt)
                            y.append(weekdata[str(day)][userID]["RW"])
                if day > changedate and change_cnt == -1:
                    change_cnt = cnt
                cnt += 1
            if str(day) in weekdata and str(day) == str(changedate):
                change_cnt = cnt
                cnt += 1

    data = pd.DataFrame({'y': y, 'x': x})

    data_rdd = rdd.truncated_data(data, 'x', bandwidth, cut=change_cnt)

    model = rdd.rdd(data_rdd, 'x', 'y', cut=change_cnt)

    results[str(changedate)]["TREATED"] = round(model.fit().params[1], 4)
    results[str(changedate)]["p"] = round(model.fit().pvalues[1], 4)
    results[str(changedate)]["a"] = round(model.fit().conf_int(alpha=0.05)[0][1], 4)
    results[str(changedate)]["b"] = round(model.fit().conf_int(alpha=0.05)[1][1], 4)

    cnt += 1
    if cnt%10 == 0:
        logging.info(str(cnt) + " models computed (" + str(100*(cnt/len(changedate))) + "%).")

logging.info("Done. (3/4)")



logging.info("Saving results ...")

with open(path_results, "w") as fp:
    json.dump(results, fp)

logging.info("Done. (4/4)")



log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))