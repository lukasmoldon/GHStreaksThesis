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
path_source_usergroupsize = "/home/lmoldon/data/usergroupsize.json"
path_source_genderdata = "/home/lmoldon/data/users_gender.json"
path_user_restriction = ""
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/results/streakValues.json"
# ------------------------------


# ---------- CONFIG ------------
threshold = 50  # minimum streak length to get plotted

# if != "" only compute data for userIDs in user_restriction file (path)
path_user_restriction = ""

# "male" or "female" or "",  if == "" all users
gender_restriction = ""

# ~~~~~~~~~~~~ MODE ~~~~~~~~~~~~
# mode for plot avg streak length 0 OR 1:
# 0 = count streaks today with value < threshold if they will reach length over theshold in future AND divide by usersize today
# 1 = only count streaks if value > threshold AND divide by usersize today-(threshold-1)
mode = 0
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

showdata = False  # Print plotdata in console (for debugging)?
savedata = True  # Save the resulting plot data at path_results_plot?
showcoverage = True  # Show streak coverage?
observedtime_start = date(2015, 1, 1)
observedtime_end = date(2018, 1, 1)
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
plotdata = {}  # key = day in observedtime, value = value of selected mode
start = date(1970, 1, 1)
end = date(1970, 1, 1)
# after this day everyone of observed usergroup joined GitHub
maxday_usergroupsize = date(1970, 1, 1)
# before this day nobody of observed usergroup joined GitHub
minday_usergroupsize = date(2099, 1, 1)
cnt_streaks = 0  # total number of streaks
cnt_streaks_survived = 0  # number of streaks observed in plot
# ------------------------------


log_starttime = datetime.datetime.now()


def daterange(observedtime_start, observedtime_end):
    for n in range(int((observedtime_end - observedtime_start).days + 1)):
        yield observedtime_start + timedelta(n)


for single_date in daterange(observedtime_start, observedtime_end):
    plotdata[str(single_date.strftime("%Y-%m-%d"))] = 0


logging.info("Loading data ...")
with open(path_source_streakdata, "r") as fp:
    streakdata = json.load(fp)
if path_user_restriction != "" or gender_restriction != "":
    with open(path_source_userdata, "r") as fp:
        userdata = json.load(fp)
if path_user_restriction != "":
    with open(path_user_restriction, "r") as fp:
        userids_restricted = json.load(fp)
if gender_restriction != "":
    with open(path_source_genderdata, "r") as fp:
        genderdata = json.load(fp)
logging.info("Done (1/5)")


logging.info("Comuting user set ...")

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

for userid in delIDs:
    del streakdata[userid]

logging.info("Done. (2/5)")


logging.info("Computing usergroupsize data ...")

if path_user_restriction == "" and gender_restriction == "":
    with open(path_source_usergroupsize, "r") as fp:
        usergroupsize = json.load(fp)
else:
    usergroupsize = {}

    for day in daterange(observedtime_start, observedtime_end):
        usergroupsize[str(day)] = 0

    for userid in streakdata:
        if userid in userdata:
            created = datetime.datetime.strptime(str(userdata[userid]["created_at"]), "%Y-%m-%d %H:%M:%S").date()
            if created >= observedtime_start and created <= observedtime_end:
                for day in daterange(created, observedtime_end):
                    usergroupsize[str(day)] += 1
            elif created < observedtime_start:
                for day in daterange(observedtime_start, observedtime_end):
                    usergroupsize[str(day)] += 1

for entry in usergroupsize:
    thisday = datetime.datetime.strptime(str(entry), datetimeFormat).date()
    if thisday > maxday_usergroupsize:
        maxday_usergroupsize = thisday
    if thisday < minday_usergroupsize:
        minday_usergroupsize = thisday

logging.info("Done. (3/5)")


logging.info("Starting ...")
for userid in streakdata:
    for streakid in streakdata[userid]:

        start = datetime.datetime.strptime(str(streakdata[userid][streakid]["start"]), datetimeFormat).date()
        end = datetime.datetime.strptime(str(streakdata[userid][streakid]["end"]), datetimeFormat).date()
        length = int(streakdata[userid][streakid]["len"])

        cnt_streaks += 1
        if cnt_streaks % 1000000 == 0:
            logging.info(str(cnt_streaks/1000000) + " million streaks computed.")

        if length >= threshold:
            # streak happend (partially) in observed time
            if start <= observedtime_end and end >= observedtime_start:
                cnt_streaks_survived += 1
                if start >= observedtime_start:  # start in observed time
                    if end <= observedtime_end:  # start and end in observed time
                        for single_date in daterange(start, end):
                            if mode == 0:
                                plotdata[str(single_date)] += ((single_date - start) + timedelta(days=1)).days
                            elif mode == 1:
                                if single_date >= (start + timedelta(days=threshold-1)):
                                    plotdata[str(single_date)] += ((single_date - start) + timedelta(days=1)).days
                    else:  # start in observed time, end not in observed time
                        for single_date in daterange(start, observedtime_end):
                            if mode == 0:
                                plotdata[str(single_date)] += ((single_date - start) + timedelta(days=1)).days
                            elif mode == 1:
                                if single_date >= (start + timedelta(days=threshold-1)):
                                    plotdata[str(single_date)] += ((single_date - start) + timedelta(days=1)).days
                else:  # start not in observed time
                    if end <= observedtime_end:  # start not in observed time, but end in observed time
                        for single_date in daterange(observedtime_start, end):
                            if mode == 0:
                                plotdata[str(single_date)] += ((single_date - start) + timedelta(days=1)).days
                            elif mode == 1:
                                if single_date >= (start + timedelta(days=threshold-1)):
                                    plotdata[str(single_date)] += ((single_date - start) + timedelta(days=1)).days
                    else:  # start and end not in observed time
                        for single_date in daterange(observedtime_start, observedtime_end):
                            if mode == 0:
                                plotdata[str(single_date)] += ((single_date - start) + timedelta(days=1)).days
                            elif mode == 1:
                                if single_date >= (start + timedelta(days=threshold-1)):
                                    plotdata[str(single_date)] += ((single_date - start) + timedelta(days=1)).days
logging.info("Done. (4/5)")


logging.info("Creating plot data ...")

if mode == 0:
    for entry in plotdata:  # divide by usergroupsize
        thisday = datetime.datetime.strptime(str(entry), datetimeFormat).date()
        if str(thisday) in usergroupsize:
            plotdata[entry] = (plotdata[entry] / usergroupsize[str(thisday)])
        elif thisday > maxday_usergroupsize:
            plotdata[entry] = (plotdata[entry] / usergroupsize[str(maxday_usergroupsize)])
        elif thisday < minday_usergroupsize:
            del plotdata[entry]
        else:
            logging.critical("Error with date: " + str(thisday))
            del plotdata[entry]
elif mode == 1:
    for entry in plotdata:  # divide by usergroupsize
        thisday = datetime.datetime.strptime(str(entry), datetimeFormat).date()
        # each user had to join until that day to have a chance for a streak of length <threshold> at <thisday>
        latestJoinDay = thisday - timedelta(days=threshold-1)
        if str(latestJoinDay) in usergroupsize:
            plotdata[entry] = (plotdata[entry] / usergroupsize[str(latestJoinDay)])
        elif latestJoinDay > maxday_usergroupsize:
            plotdata[entry] = (plotdata[entry] / usergroupsize[str(maxday_usergroupsize)])
        elif latestJoinDay < minday_usergroupsize:
            del plotdata[entry]
        else:
            logging.critical("Error with date: " + str(thisday))
            del plotdata[entry]


if savedata:
    with open(path_results, "w") as fp:
        json.dump(plotdata, fp)
    logging.info("Plot data saved.")

if showdata:
    logging.info("Data:")
    print(plotdata)

if showcoverage:
    logging.info("Streaks total: " + str(cnt_streaks))
    logging.info("Streaks in plot: " + str(cnt_streaks_survived))
    logging.info(str((cnt_streaks_survived / cnt_streaks) * 100) + "%" + " coverage of reduced_users streaks in plot.")


logging.info("Done. (5/5)")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))
