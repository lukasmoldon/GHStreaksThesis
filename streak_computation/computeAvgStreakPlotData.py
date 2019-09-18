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
path_source_streakdata = "/home/lmoldon/data/user_streaks.json"
path_source_groupdata = "/home/lmoldon/data/user_groups.json"
path_source_usergroupsize = "/home/lmoldon/data/usergroupsize.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/results/streakValues.json"
# ------------------------------


# ---------- CONFIG ------------
threshold = 50 # minimum streak length to get plotted

# ~~~~~~~~~~~~ MODE ~~~~~~~~~~~~
# mode for plot avg streak length 0 OR 1: 
# 0 = count streaks today with value < threshold if they will reach length over theshold in future AND divide by usersize today
# 1 = only count streaks if value > threshold AND divide by usersize today-(threshold-1)
mode = 0 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

showdata = False # Print plotdata in console (for debugging)?
savedata = True # Save the resulting plot data at path_results_plot?
showcoverage = True # Show streak coverage?
observedtime_start = date(2015, 1, 1)
observedtime_end = date(2018, 1, 1)
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
plotdata = {} # key = day in observedtime, value = value of selected mode
start = date(1970, 1, 1)
end = date(1970, 1, 1)
maxday_usergroupsize = date(1970, 1, 1) # after this day everyone of observed usergroup joined GitHub
minday_usergroupsize = date(2099, 1, 1) # before this day nobody of observed usergroup joined GitHub
cnt_streaks = 0 # total number of streaks
cnt_streaks_survived = 0 # number of streaks observed in plot
# ------------------------------



log_starttime = datetime.datetime.now()

def daterange(observedtime_start, observedtime_end):
        for n in range(int((observedtime_end - observedtime_start).days)):
                yield observedtime_start + timedelta(n)


for single_date in daterange(observedtime_start, observedtime_end):
        plotdata[str(single_date.strftime("%Y-%m-%d"))] = 0


logging.info("Accessing usergroupsize data ...")
with open(path_source_usergroupsize, "r") as fp:
    usergroupsize = json.load(fp)

for entry in usergroupsize:
    thisday = datetime.datetime.strptime(str(entry), datetimeFormat).date()
    if thisday > maxday_usergroupsize:
        maxday_usergroupsize = thisday
    if thisday < minday_usergroupsize:
        minday_usergroupsize = thisday

logging.info("Done. (1/4)")


logging.info("Accessing usergroup data ...")
with open(path_source_groupdata, "r") as fp:
    groupdata = json.load(fp)

logging.info("Done. (2/4)")


logging.info("Starting ...")
streakdata = ijson.parse(open(path_source_streakdata, "r"))
for prefix, event, value in streakdata:
    if ".start" in prefix:
        start = datetime.datetime.strptime(str(value), datetimeFormat).date()
        cnt_streaks += 1
        if cnt_streaks % 1000000 == 0: 
            logging.info(str(cnt_streaks/1000000) + " million streaks computed.")
    elif ".end" in prefix:
        end = datetime.datetime.strptime(str(value), datetimeFormat).date()
    elif ".len" in prefix:
        if int(value) >= threshold:
                if start <= observedtime_end and end >= observedtime_start: # streak happend (partially) in observed time
                    cnt_streaks_survived += 1
                    if start >= observedtime_start: # start in observed time
                            if end <= observedtime_end: # start and end in observed time
                                    for single_date in daterange(start, end):
                                        if mode == 0:
                                            plotdata[str(single_date)] += ((single_date - start) + timedelta(days=1)).days
                                        elif mode == 1:
                                            if single_date >= (start + timedelta(days=threshold-1)):
                                                plotdata[str(single_date)] += ((single_date - start) + timedelta(days=1)).days
                            else: # start in observed time, end not in observed time
                                    for single_date in daterange(start, observedtime_end):
                                            if mode == 0:
                                                plotdata[str(single_date)] += ((single_date - start) + timedelta(days=1)).days
                                            elif mode == 1:
                                                if single_date >= (start + timedelta(days=threshold-1)):
                                                    plotdata[str(single_date)] += ((single_date - start) + timedelta(days=1)).days
                    else: # start not in observed time
                            if end <= observedtime_end: # start not in observed time, but end in observed time
                                    for single_date in daterange(observedtime_start, end):
                                            if mode == 0:
                                                plotdata[str(single_date)] += ((single_date - start) + timedelta(days=1)).days
                                            elif mode == 1:
                                                if single_date >= (start + timedelta(days=threshold-1)):
                                                    plotdata[str(single_date)] += ((single_date - start) + timedelta(days=1)).days
                            else: # start and end not in observed time
                                    for single_date in daterange(observedtime_start, observedtime_end):
                                            if mode == 0:
                                                plotdata[str(single_date)] += ((single_date - start) + timedelta(days=1)).days
                                            elif mode == 1:
                                                if single_date >= (start + timedelta(days=threshold-1)):
                                                    plotdata[str(single_date)] += ((single_date - start) + timedelta(days=1)).days
logging.info("Done. (3/4)")


logging.info("Creating plot data ...")

if mode == 0:
    for entry in plotdata: # divide by usergroupsize 
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
    for entry in plotdata: # divide by usergroupsize 
        thisday = datetime.datetime.strptime(str(entry), datetimeFormat).date()
        latestJoinDay = thisday - timedelta(days=threshold-1) # each user had to join until that day to have a chance for a streak of length <threshold> at <thisday>
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


logging.info("Done. (4/4)")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))