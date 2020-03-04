# ---------- IMPORT ------------
import logging
import matplotlib
import matplotlib.pyplot as plt
import datetime
import json
import ijson
from datetime import timedelta, date
# ------------------------------


# ---------- INPUT -------------
path_source_userdata = "/home/lmoldon/data/users_reduced.json"
path_source_streakdata = "/home/lmoldon/data/user_streaks.json"
path_source_usergroupsize = "/home/lmoldon/data/usergroupsizeALL.json"
path_source_genderdata = "/home/lmoldon/data/users_gender.json"
path_source_merge = "/home/lmoldon/data/merge.json"
path_user_restriction = ""
# ------------------------------


# ---------- OUTPUT ------------
# RENAME IF RESTRICTION IS ACTIVE TO AVOID OVERRIDE
path_results = "/home/lmoldon/results/streakShareValues.json"
# ------------------------------


# ---------- CONFIG ------------
thresholds = [20, 60, 200]  # minimum streak length to get plotted
totalvalues = False

# if != "" only compute data for userIDs in user_restriction file (path)
path_user_restriction = ""

# "male" or "female" or "",  if == "" all users
gender_restriction = ""

# e.g. ["USA", "China"] or ["Germany"]
country_restriction = []

observedtime_start = date(2015, 1, 1)
observedtime_end = date(2018, 1, 1)
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
plotdata = {}  # key = day in observedtime, value = value of selected mode
# ------------------------------



log_starttime = datetime.datetime.now()



def daterange(observedtime_start, observedtime_end):
    for n in range(int((observedtime_end - observedtime_start).days + 1)):
        yield observedtime_start + timedelta(n)



for threshold in thresholds:

    plotdata[str(threshold)] = {}

    for single_date in daterange(observedtime_start, observedtime_end):
        plotdata[str(threshold)][str(single_date.strftime("%Y-%m-%d"))] = 0



logging.info("Loading data ...")
with open(path_source_streakdata, "r") as fp:
    streakdata = json.load(fp)
if path_user_restriction != "" or gender_restriction != "" or country_restriction != []:
    with open(path_source_userdata, "r") as fp:
        userdata = json.load(fp)
if path_user_restriction != "":
    with open(path_user_restriction, "r") as fp:
        userids_restricted = json.load(fp)
if gender_restriction != "" or country_restriction != []:
    with open(path_source_genderdata, "r") as fp:
        genderdata = json.load(fp)
    with open(path_source_merge, "r") as fp:
        merge = json.load(fp)
logging.info("Done (1/5)")



logging.info("Comuting user set ...")

if path_user_restriction != "" or gender_restriction != "" or country_restriction != []:

    delIDs = set()

    if path_user_restriction != "":
        for userid in streakdata:
            if userid not in userids_restricted:
                delIDs.add(userid)

    if gender_restriction != "":
        for userid in streakdata:
            if userid not in genderdata:
                delIDs.add(userid)
            elif genderdata[userid]["gender"] != gender_restriction:
                delIDs.add(userid)
    
    if country_restriction != []:
        for userid in streakdata:
            if userid not in genderdata:
                delIDs.add(userid)
            else:
                if genderdata[userid]["country"] in merge:
                    genderdata[userid]["country"] = merge[genderdata[userid]["country"]]
                if genderdata[userid]["country"] not in country_restriction:
                    delIDs.add(userid)

    for userid in delIDs:
        del streakdata[userid]

logging.info("Done. (2/5)")



logging.info("Computing usergroupsize data ...")

if path_user_restriction == "" and gender_restriction == "" and country_restriction == []:
    with open(path_source_usergroupsize, "r") as fp:
        usergroupsize = json.load(fp)
else:
    usergroupsize = {}

    for day in daterange((observedtime_start-timedelta(days=max(thresholds)-1)), observedtime_end):
        usergroupsize[str(day)] = 0

    for userid in streakdata:
        if userid in userdata:
            created = datetime.datetime.strptime(str(userdata[userid]["created_at"]), "%Y-%m-%d %H:%M:%S").date()
            if created >= (observedtime_start-timedelta(days=max(thresholds)-1)) and created <= observedtime_end:
                for day in daterange(created, observedtime_end):
                    usergroupsize[str(day)] += 1
            elif created < (observedtime_start-timedelta(days=max(thresholds)-1)):
                for day in daterange((observedtime_start-timedelta(days=max(thresholds)-1)), observedtime_end):
                    usergroupsize[str(day)] += 1

logging.info("Done. (3/5)")



logging.info("Starting ...")

cnt_streaks = 0

for userid in streakdata:
    for streakid in streakdata[userid]:

        start = datetime.datetime.strptime(str(streakdata[userid][streakid]["start"]), datetimeFormat).date()
        end = datetime.datetime.strptime(str(streakdata[userid][streakid]["end"]), datetimeFormat).date()
        length = int(streakdata[userid][streakid]["len"])

        cnt_streaks += 1
        if cnt_streaks % 1000000 == 0:
            logging.info(str(cnt_streaks/1000000) + " million streaks computed.")

        for threshold in thresholds:

            if length >= threshold:
                # streak happend (partially) in observed time
                if start <= observedtime_end and end >= observedtime_start:

                    a = max((start+timedelta(days=threshold-1)), observedtime_start)
                    b = min(end, observedtime_end)

                    for day in daterange(a, b):
                        plotdata[str(threshold)][str(day)] += 1

logging.info("Done. (4/5)")



logging.info("Creating plot data ...")

if not totalvalues:
    for threshold in thresholds:
        for day in daterange(observedtime_start, observedtime_end):
            if usergroupsize[str(day-timedelta(days=threshold-1))] > 0:
                plotdata[str(threshold)][str(day)] /= usergroupsize[str(day-timedelta(days=threshold-1))]
            else:
                plotdata[str(threshold)][str(day)] = 0

with open(path_results, "w") as fp:
    json.dump(plotdata, fp)
logging.info("Plot data saved.")

logging.info("Done. (5/5)")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))
