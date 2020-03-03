# ---------- IMPORT ------------
import logging
import datetime
import json
from datetime import timedelta, date
# ------------------------------


# ---------- INPUT -------------
path_source_streakdata = "/home/lmoldon/data/user_streaks.json"
path_source_subpopulation = ".."
# ------------------------------


# ---------- OUTPUT ------------
path_results = ".."
# ------------------------------


# ---------- CONFIG ------------
year = "2015"
minlen = 15
useSubpopulation = False # refers to ActiveSubpopulation file
# counting streaks from the day they pass the threshold (False) or from the starting day (True)
lookIntoFuture = False
# ------------------------------


# ---------- INITIAL -----------
datetimeFormat = "%Y-%m-%d"
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
path_source_subpopulation = "/home/lmoldon/data/activeSubpopulation" + year + ".json"
path_results_active = "/home/lmoldon/results/activeStreaks" + year + ".json"
path_results_activeRecords = "/home/lmoldon/results/activeStreakRecords" + year + ".json"
observed_start = datetime.datetime.strptime(year + "-01-01", datetimeFormat).date()
observed_end = datetime.datetime.strptime(year + "-12-31", datetimeFormat).date()
lastRecord = {} # before observed time
records = {} # while observed time
records_order = {}
activeStreaks = {}
activeStreakRecords = {}
# ------------------------------



def daterange(observedtime_start, observedtime_end):
        for n in range(int((observedtime_end - observedtime_start).days + 1)):
                yield observedtime_start + timedelta(n)



log_starttime = datetime.datetime.now()

logging.info("Loading data ...")
with open(path_source_streakdata, "r") as fp:
    streakdata = json.load(fp)

if useSubpopulation:
    with open(path_source_subpopulation, "r") as fp:
        userids = json.load(fp)

    delIDs= set()
    for userid in streakdata:
        if userid not in userids:
            delIDs.add(userid)
    for userid in delIDs:
        del streakdata[userid]

for single_date in daterange(observed_start, observed_end):
    activeStreaks[str(single_date)] = 0
    activeStreakRecords[str(single_date)] = 0
logging.info("Done (1/3)")


logging.info("Starting A...")
cnt_streaks_total = 0
## FIND MAX RECORD IN THE PAST BEFORE OBSERVED TIME ##
for userid in streakdata:  # for each user in subpopulation

    lastRecord[userid] = minlen

    for streakid in streakdata[userid]:  # for each streak of that user

        start = datetime.datetime.strptime(str(streakdata[userid][streakid]["start"]), datetimeFormat).date()
        end = datetime.datetime.strptime(str(streakdata[userid][streakid]["end"]), datetimeFormat).date()
        length = int(streakdata[userid][streakid]["len"])

        cnt_streaks_total += 1
        if cnt_streaks_total % 1000000 == 0:
            logging.info(str(cnt_streaks_total/1000000) + " million streaks computed.")

        if length >= lastRecord[userid] and end < observed_start: # streak could be last max streak before observed time
            lastRecord[userid] = length # get maximum streak length of the past
        

logging.info("Starting B...")
cnt_streaks_total = 0        
## FIND NEW RECORDS IN OBSERVED TIME INCULDING ORDERING##
for userid in streakdata:  # for each user in subpopulation

    records[userid] = {}
    records_order[userid] = {}
    first_start = observed_start

    for streakid in streakdata[userid]:  # for each streak of that user

        start = datetime.datetime.strptime(str(streakdata[userid][streakid]["start"]), datetimeFormat).date()
        end = datetime.datetime.strptime(str(streakdata[userid][streakid]["end"]), datetimeFormat).date()
        length = int(streakdata[userid][streakid]["len"])

        cnt_streaks_total += 1
        if cnt_streaks_total % 1000000 == 0:
            logging.info(str(cnt_streaks_total/1000000) + " million streaks computed.")

        if length >= lastRecord[userid] and start <= observed_end and end >= observed_start: # streak happend (partially) in observed time
            records[userid][str(start)] = length
            if start < first_start:
                first_start = start

    # Get ordering and delete wrong records
    lastmax = lastRecord[userid]
    pos = 1
    for day in daterange(first_start, observed_end):
        if str(day) in records[userid]:
            if records[userid][str(day)] > lastmax:
                lastmax = records[userid][str(day)]
                records_order[userid][str(day)] = pos
                pos += 1
            else:
                # Delete streaks longer than initial record (before) but not longer than record in between
                del records[userid][str(day)]


logging.info("Starting C...")
cnt_streaks_total = 0            
## CALCULATE TOTAL VALUES (RECORD AND MINLENGTH) ##
for userid in streakdata:  # for each user in subpopulation

    for streakid in streakdata[userid]:  # for each streak of that user

        start = datetime.datetime.strptime(str(streakdata[userid][streakid]["start"]), datetimeFormat).date()
        end = datetime.datetime.strptime(str(streakdata[userid][streakid]["end"]), datetimeFormat).date()
        length = int(streakdata[userid][streakid]["len"])

        cnt_streaks_total += 1
        if cnt_streaks_total % 1000000 == 0:
            logging.info(str(cnt_streaks_total/1000000) + " million streaks computed.")

        if length >= minlen and start <= observed_end and end >= observed_start: # streak happend (partially) in observed time

            if start >= observed_start:  # start in observed time
                if end <= observed_end:  # start and end in observed time
                    cur_start = start
                    cur_end = end
                else:  # start in observed time, end not in observed time
                    cur_start = start
                    cur_end = observed_end                              
            else: # start not in observed time
                if end <= observed_end: # start not in observed time, but end in observed time
                    cur_start = observed_start
                    cur_end = end
                else: # start and end not in observed time
                    cur_start = observed_start
                    cur_end = observed_end

            # all streaks with min length
            for single_date in daterange(cur_start, cur_end):
                if not lookIntoFuture:
                    if ((single_date - start) + timedelta(days=1)).days >= minlen:
                        activeStreaks[str(single_date)] += 1
                else:
                    activeStreaks[str(single_date)] += 1
            # all records
            if str(start) in records[userid]: # this streak was a new record
                if not lookIntoFuture:
                    if records_order[userid][str(start)] == 1: # first new record in observed time
                        for single_date in daterange(cur_start, cur_end):
                            if ((single_date - start) + timedelta(days=1)).days >= lastRecord[userid]:
                                activeStreakRecords[str(single_date)] += 1
                    else: # record before was also in observed time
                        for key in records_order[userid]:
                            if records_order[userid][key] == records_order[userid][str(start)]-1: # record before found
                                for single_date in daterange(cur_start, cur_end):
                                    if ((single_date - start) + timedelta(days=1)).days >= records[userid][key]:
                                        activeStreakRecords[str(single_date)] += 1
                else:
                    for single_date in daterange(cur_start, cur_end):
                        activeStreakRecords[str(single_date)] += 1

                                

logging.info("Done. (2/3)")


logging.info("Saving results ...")
with open(path_results_active, "w") as fp:
    json.dump(activeStreaks, fp)

with open(path_results_activeRecords, "w") as fp:
    json.dump(activeStreakRecords, fp)
logging.info("Done. (3/3)")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))