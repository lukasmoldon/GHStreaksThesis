# ---------- IMPORT ------------
import logging
import datetime
import json
from datetime import timedelta, date
import numpy as np
import random
import scipy.stats
# ------------------------------


# ---------- INPUT -------------
path_source_streakdata = "/home/lmoldon/data/user_streaks.json"
path_source_userdata = "/home/lmoldon/data/users_reduced.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = ".."
# ------------------------------


# ---------- CONFIG ------------
before = True
minlen = 25
maxdistance = 30 # distance between end of last record and start of second streak
timerange = 6 # 2x timerange (for before after 0) + 1 (for 0) - 2 (for border) represents x-axis
confidenceInterval = 95 # in %
amountSamples = 1000 # number of bootstrapped samples per day
# ------------------------------


# ---------- INITIAL -----------
datetimeFormat = "%Y-%m-%d"
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
survivalcounts = {}
survivalrates = {}
lastRecord = {} # before observed time
records = {} # while observed time
total_observed = 0
users_observed = 0
lowerbound = (100 - confidenceInterval) / 2
upperbound = confidenceInterval + (100 - confidenceInterval) / 2
if before:
    path_results = "/home/lmoldon/results/survivalAroundLastRecordMIN" + str(minlen) + "DIST" + str(maxdistance) + "BEFORE_ERRORB.json"
    observed_start = datetime.datetime.strptime("2013-01-01", datetimeFormat).date()
    observed_end = datetime.datetime.strptime("2016-05-18", datetimeFormat).date()
else:
    path_results = "/home/lmoldon/results/survivalAroundLastRecordMIN" + str(minlen) + "DIST" + str(maxdistance) + "AFTER_ERRORB.json"
    observed_start = datetime.datetime.strptime("2016-05-19", datetimeFormat).date()
    observed_end = datetime.datetime.strptime("2019-04-01", datetimeFormat).date()
# ------------------------------



def daterange(observedtime_start, observedtime_end):
        for n in range(int((observedtime_end - observedtime_start).days + 1)):
                yield observedtime_start + timedelta(n)


def createBootstrapSample(data):
    i = 0
    bootstrapSample = []
    while i < len(data):
        bootstrapSample.append(random.choice(data))
        i += 1
    return bootstrapSample

def getBootstrapSampleAvgs(survived, abandoned, amountSamples):
    sampleAvgs = []
    base = [1] * survived + [0] * abandoned
    random.shuffle(base)
    i = 0
    while i < amountSamples:
        sampleAvgs.append(np.mean(createBootstrapSample(base)))
        i += 1
    return sampleAvgs



log_starttime = datetime.datetime.now()

logging.info("Loading data ...")
with open(path_source_streakdata, "r") as fp:
    streakdata = json.load(fp)

with open(path_source_userdata, "r") as fp:
    userids = json.load(fp)

logging.info("Done (1/3)")


i = timerange * -1
while i <= timerange:
    survivalcounts[str(i)] = 0
    i += 1

deleteIDs = set()
for userid in userids:
    if userid not in streakdata:
        deleteIDs.add(userid)

for userid in deleteIDs:
    del userids[userid]


logging.info("Starting A...")
cnt_streaks_total = 0
## FIND MAX RECORD IN THE PAST BEFORE OBSERVED TIME ##
for userid in userids:  # for each user

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
## FIND NEW RECORDS IN OBSERVED TIME ##
for userid in userids:  # for each user in subpopulation

    records[userid] = {}
    first_start = observed_start

    for streakid in streakdata[userid]:  # for each streak of that user

        start = datetime.datetime.strptime(str(streakdata[userid][streakid]["start"]), datetimeFormat).date()
        end = datetime.datetime.strptime(str(streakdata[userid][streakid]["end"]), datetimeFormat).date()
        length = int(streakdata[userid][streakid]["len"])

        cnt_streaks_total += 1
        if cnt_streaks_total % 1000000 == 0:
            logging.info(str(cnt_streaks_total/1000000) + " million streaks computed.")

        if length >= lastRecord[userid] and end >= observed_start and end <= observed_end: # streak end is in observed time
            records[userid][str(start)] = length
            if start < first_start:
                first_start = start

    # Delete streaks longer than initial record (before) but not longer than record in between
    lastmax = lastRecord[userid]
    for day in daterange(first_start, observed_end):
        if str(day) in records[userid]:
            if records[userid][str(day)] > lastmax:
                lastmax = records[userid][str(day)]
            else:
                del records[userid][str(day)]


logging.info("Starting C...")
cnt_streaks_total = 0            
## CALCULATE VALUES ##
for userid in userids:  # for each user in subpopulation

    used = False

    for streakid in streakdata[userid]:  # for each streak of that user

        start = datetime.datetime.strptime(str(streakdata[userid][streakid]["start"]), datetimeFormat).date()
        end = datetime.datetime.strptime(str(streakdata[userid][streakid]["end"]), datetimeFormat).date()
        length = int(streakdata[userid][streakid]["len"])

        cnt_streaks_total += 1
        if cnt_streaks_total % 1000000 == 0:
            logging.info(str(cnt_streaks_total/1000000) + " million streaks computed.")

        if length >= minlen and end >= observed_start and end <= observed_end: # streak end is in observed time

            for recordstart in records[userid]:
                distance = (start - datetime.datetime.strptime(recordstart, datetimeFormat).date()).days - int(records[userid][recordstart]) # - length for distance between end and new start
                if distance > 0 and distance <= maxdistance: # within maxdistance days next streak after any record
                    if (int(records[userid][recordstart] - length) >= (timerange * -1)): # within the x-axis 
                        total_observed += 1
                        used = True
                        i = timerange * -1
                        while i <= (length - int(records[userid][recordstart])) and i <= timerange:
                            survivalcounts[str(i)] += 1
                            i += 1

    if used:
        users_observed += 1
                        
# Calculate prob for streak surviving
i = timerange * -1
while i < (timerange - 1):
    
    cnt_survived = survivalcounts[str(i+1)] # #survived (contribution on day X - 1, contribution on day X)
    cnt_abandoned = survivalcounts[str(i)] - survivalcounts[str(i+1)] # #abandoned (contribution on day X - 1, no contribution on day X)

    sampleAvgs = getBootstrapSampleAvgs(cnt_survived, cnt_abandoned, amountSamples)

    survivalrates[str(i+1)] = {
        "r": (survivalcounts[str(i+1)] / survivalcounts[str(i)]), # survival rate
        "0": cnt_abandoned,
        "1": cnt_survived,
        "a": np.percentile(sampleAvgs, lowerbound), # 2.5th% of x bootstrapped avg values (lower bound of 95% confidence interval)
        "b": np.percentile(sampleAvgs, upperbound)  # 97.5th% of x bootstrapped avg values (upper bound of 95% confidence interval)
    }
    i += 1

survivalrates["__TOTAL__"] = total_observed   
survivalrates["__USERS__"] = users_observed

logging.info("Done. (2/3)")


logging.info("Saving results ...")
with open(path_results, "w") as fp:
    json.dump(survivalrates, fp)
logging.info("Done. (3/3)")

logging.info("Total number of observed streaks after records: " + str(total_observed))

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))