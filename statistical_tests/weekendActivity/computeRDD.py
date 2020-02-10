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
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
observed_start = date(2016,1,1)
observed_end = date(2016,12,31)
userlevel = True # True: datapoint represents single user per day, False: represents avg of all users per day
bandwidth = 52/2 # bandwidth +/- around cut (2x for bandwidth length) => maximum is 52/2
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
changedate = date(2016,5,16)
x = []
y = []
if userlevel:
    path_source = "/home/lmoldon/results/weekendActivity_userlevel.json"
else:
    path_source = "/home/lmoldon/results/weekendActivity.json"
# ------------------------------


def daterange(observedtime_start, observedtime_end):
        for n in range(int((observedtime_end - observedtime_start).days + 1)):
                yield observedtime_start + timedelta(n)


log_starttime = datetime.datetime.now()

with open(path_source, "r") as fp:
    weekdata = json.load(fp)

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
                x.append(cnt)
                y.append(weekdata[str(day)][userID]["RW"])
            if day > changedate and change_cnt == -1:
                change_cnt = cnt
            cnt += 1

data = pd.DataFrame({'y': y, 'x': x})

#bandwidth_opt = rdd.optimal_bandwidth(data['y'], data['x'], cut=change_cnt)
#logging.info("Optimal bandwidth:" + str(bandwidth_opt))

data_rdd = rdd.truncated_data(data, 'x', bandwidth, cut=change_cnt)

model = rdd.rdd(data_rdd, 'x', 'y', cut=change_cnt)
logging.info(model.fit().summary())

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))