# ---------- IMPORT ------------
import logging
import datetime
from datetime import date, timedelta
import json
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
# ------------------------------


# ---------- INPUT -------------
path_source = "..."
path_source_genderdata = "C:/Users/Lukas/Desktop/users_gender.json"
path_source_merge = "C:/Users/Lukas/Desktop/merge.json"
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
observed_start = date(2016, 4, 25)
observed_end = date(2016, 6, 19)
userlevel = True # True: datapoint represents single user per day, False: represents avg of all users per day
bandwidth = 3 # bandwidth +/- around cut (2x for bandwidth length) => maximum is 52/2
country = "" # restrict rdd on users from a specific country, if empty streak -  disable feature (ONLY FOR USERLEVEL = TRUE)
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
changedate = date(2016,5,16)
x = []
y = []
if userlevel:
    path_source = "C:/Users/Lukas/Desktop/weekendActivity_userlevel.json"
else:
    path_source = "C:/Users/Lukas/Desktop/weekendActivity.json"
# ------------------------------


def daterange(observedtime_start, observedtime_end):
        for n in range(int((observedtime_end - observedtime_start).days + 1)):
                yield observedtime_start + timedelta(n)


log_starttime = datetime.datetime.now()

with open(path_source, "r") as fp:
    weekdata = json.load(fp)

with open(path_source_genderdata, "r") as fp:
    genderdata = json.load(fp)

with open(path_source_merge, "r") as fp:
    merge = json.load(fp)

del weekdata["2016-04-18"]
del weekdata["2016-05-16"]
del weekdata["2016-06-13"]

if country != "":
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

cnt = 1 # index of current week
change_cnt = -1 # index of first week after the change = cut
if not userlevel:
    for day in daterange(observed_start, observed_end):
        if str(day) in weekdata:
            x.append(cnt)
            y.append(weekdata[str(day)]["RW"])
            if day > changedate and change_cnt == -1:
                change_cnt = cnt
            cnt += 1
else:
    for day in daterange(observed_start, observed_end):
        if str(day) in weekdata:
            for userID in weekdata[str(day)]:
                if country == "" or genderdata[userID]["country"] == country:
                    x.append(cnt)
                    y.append(weekdata[str(day)][userID]["RW"])
            if day > changedate and change_cnt == -1:
                change_cnt = cnt
            cnt += 1


rdd_before_x = list(range(1, change_cnt))
rdd_before_y = [0.2016+0.0004*el for el in rdd_before_x]
rdd_before_x[-1] += 0.5
rdd_after_x = list(range(change_cnt-1, cnt))
rdd_after_y = [0.2016+0.0004*el-0.0241 for el in rdd_after_x]
rdd_after_x[0] += 0.5
    
plt.scatter(x,y, s=0.0001, color='#17719B')
plt.plot(rdd_before_x, rdd_before_y, color='#32A875', label='RDD')
plt.plot(rdd_after_x, rdd_after_y, color='#32A875')
plt.xlabel("Week", fontsize=13)
plt.ylabel("ratio of weekend activity per user", fontsize=13)
plt.axvline(x=change_cnt-0.5, color="r", label="Changedate")
plt.legend()
plt.show()

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))