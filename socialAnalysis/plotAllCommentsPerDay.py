# ---------- IMPORT ------------
import logging
import datetime
import json
import datetime
from datetime import timedelta, date
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
# ------------------------------


# ---------- INPUT -------------
path_source_commits = "C:/Users/Lukas/Desktop/commitCommentsCount.json"
path_source_pullrequests = "C:/Users/Lukas/Desktop/pullrequestCommentsCount.json"
path_source_issues = "C:/Users/Lukas/Desktop/issueCommentsCount.json"

path_source_communitysize = "C:/Users/Lukas/Desktop/communitysize_per_day.json"
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
observed_start = date(2012,1,1)
observed_end = date(2019,1,1)
total = False # total count or per user
weekly = True # plot avg per week
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
list_of_datetimes = []
values = []
# ------------------------------


def daterange(observedtime_start, observedtime_end):
        for n in range(int((observedtime_end - observedtime_start).days + 1)):
                yield observedtime_start + timedelta(n)


log_starttime = datetime.datetime.now()


logging.info("Loading data ...")
with open(path_source_commits, "r") as fp:
    data_commits = json.load(fp)
with open(path_source_pullrequests, "r") as fp:
    data_pullrequests = json.load(fp)
with open(path_source_issues, "r") as fp:
    data_issues = json.load(fp)
with open(path_source_communitysize, "r") as fp:
    community = json.load(fp)
logging.info("Done (1/2)")


logging.info("Starting ...")

if not weekly:
    for day in daterange(observed_start, observed_end):
        cnt = 0
        list_of_datetimes.append(day)

        if str(day) in data_commits:
            cnt += data_commits[str(day)]
        if str(day) in data_pullrequests:
            cnt += data_pullrequests[str(day)]
        if str(day) in data_issues:
            cnt += data_issues[str(day)]

        if total:
            values.append(cnt)
        else:
            values.append(cnt/community[str(day)])
else:
    cur_monday = observed_start
    cur_amount = 0
    for day in daterange(observed_start, observed_end):
        if day.weekday() == 0:
            list_of_datetimes.append(cur_monday)
            if total:
                values.append(cur_amount/7)
            else:
                values.append((cur_amount/7)/community[str(cur_monday)])
            cur_monday = day
            cur_amount = 0
        
        if str(day) in data_commits:
            cur_amount += data_commits[str(day)]
        if str(day) in data_pullrequests:
            cur_amount += data_pullrequests[str(day)]
        if str(day) in data_issues:
            cur_amount += data_issues[str(day)]

dates = matplotlib.dates.date2num(list_of_datetimes)
matplotlib.pyplot.plot_date(dates, values, '-')
plt.axvline(x=datetime.datetime.strptime("2016-05-19", datetimeFormat).date(), color='r', label="Streaks removed")
plt.axvline(x=datetime.datetime.strptime("2012-12-25", datetimeFormat).date(), color='g')
plt.axvline(x=datetime.datetime.strptime("2013-12-25", datetimeFormat).date(), color='g')
plt.axvline(x=datetime.datetime.strptime("2014-12-25", datetimeFormat).date(), color='g')
plt.axvline(x=datetime.datetime.strptime("2015-12-25", datetimeFormat).date(), color='g')
plt.axvline(x=datetime.datetime.strptime("2016-12-25", datetimeFormat).date(), color='g')
plt.axvline(x=datetime.datetime.strptime("2017-12-25", datetimeFormat).date(), color='g')
plt.axvline(x=datetime.datetime.strptime("2018-12-25", datetimeFormat).date(), color='g', label="Christmas")
plt.xlabel("Time")
if not weekly:
    if total:
        plt.ylabel("Total number comments on commits/issues/pull requests per day")
    else:
        plt.ylabel("Number comments on commits/issues/pull requests per user per day")
else:
    if total:
        plt.ylabel("Avg total number comments on commits/issues/pull requests per day in week")
    else:
        plt.ylabel("Avg number comments on commits/issues/pull requests per user per day in week")

plt.legend()
plt.show()

logging.info("Done (2/2)")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))