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
path_user_restriction = "/home/lmoldon/results/identifyStreakers/100DaysOfCodeUsers.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/results/goalAchiever.json"
# ------------------------------


# ---------- CONFIG ------------
thresholds = [50, 100, 105, 120]  # minimum streak length to get plotted
totalvalues = True
observedtime_start = date(2011, 1, 1)
observedtime_end = date(2019, 4, 1)
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
with open(path_source_userdata, "r") as fp:
    userdata = json.load(fp)
with open(path_user_restriction, "r") as fp:
    userids_restricted = json.load(fp)
logging.info("Done (1/5)")



logging.info("Comuting user set ...")

delIDs = set()
    
for userid in streakdata:
    if userid not in userids_restricted:
        delIDs.add(userid)

for userid in delIDs:
    del streakdata[userid]

logging.info("Done. (2/5)")



logging.info("Computing usergroupsize data ...")


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

first_hit = {}
for threshold in thresholds:
    first_hit[threshold] = {}

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

                if userid in first_hit[threshold]:
                    first_hit[threshold][userid] = min(first_hit[threshold][userid], start)
                else:
                    first_hit[threshold][userid] = start


for threshold in first_hit:
    for userid in first_hit[threshold]:
        for day in daterange(first_hit[threshold][userid], observedtime_end):
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
