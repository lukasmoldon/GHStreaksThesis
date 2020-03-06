# ---------- IMPORT ------------
import logging
import datetime
from datetime import date, timedelta
import json
import numpy as np
import random
# ------------------------------


# ---------- INPUT -------------
path_source = "/home/lmoldon/data/mutualFriendsStarting.json"
path_source_streakdata = "/home/lmoldon/data/user_streaks.json"
path_source_userdata = "/home/lmoldon/data/users_reduced.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/results/networkBadgeCorrelation.json"
# ------------------------------


# ---------- CONFIG ------------
observed_start = date(2015,1,1)
observed_end = date(2018,1,1)

random_model = False # draw badge value series from random user for each user

samplesize = 20000 # (users)
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
badgevalue = {} # {userID1: {day1: value1, ...}, ...}
corr = {} # {day1: avg(corr)}
# ------------------------------



log_starttime = datetime.datetime.now()



def daterange(observed_start, observed_end):
    for n in range(int((observed_end - observed_start).days + 1)):
        yield observed_start + timedelta(n)



logging.info("Loading data ...")

with open(path_source, "r") as fp:
    mutual = json.load(fp)
with open(path_source_streakdata, "r") as fp:
    streakdata = json.load(fp)
with open(path_source_userdata, "r") as fp:
    userdata = json.load(fp)

# remove invalid users and set 0 in badgevalue for remaining users
delIDs = set()
for userid in mutual:
    if userid in streakdata and userid in userdata:
        badgevalue[userid] = {}
        for day in daterange(observed_start, observed_end):
            badgevalue[userid][str(day)] = 0
    else:
        delIDs.add(userid)

for userid in delIDs:
    del mutual[userid]

# create user sample of length samplesize
sampleIDs = set()
delIDs = set()
while len(sampleIDs) < samplesize:
    sampleIDs.add(random.choice(list(mutual.keys())))

logging.info("Done (1/4)")



logging.info("Computing daily badge values ... ")

cnt_streaks_total = 0

for userid in sampleIDs:

    if random_model:

        # copy user properties of random user in network
        userid_random = random.choice(list(mutual.keys()))

        for streakid in streakdata[userid_random]:  # for each streak of that (copied) user
            
            start = datetime.datetime.strptime(str(streakdata[userid_random][streakid]["start"]), datetimeFormat).date()
            end = datetime.datetime.strptime(str(streakdata[userid_random][streakid]["end"]), datetimeFormat).date()
            length = int(streakdata[userid_random][streakid]["len"])

            cnt_streaks_total += 1
            if cnt_streaks_total % 1000000 == 0:
                logging.info(str(cnt_streaks_total/1000000) + " million streaks computed.")

            if start <= observed_end and end >= observed_start:

                for day in daterange(max(start, observed_start), min(end, observed_end)):

                    # copy value to origin userid from random userid
                    badgevalue[userid][str(day)] = ((day - start) + timedelta(days=1)).days
    
    else:

        for streakid in streakdata[userid]:  # for each streak of that user
            
            start = datetime.datetime.strptime(str(streakdata[userid][streakid]["start"]), datetimeFormat).date()
            end = datetime.datetime.strptime(str(streakdata[userid][streakid]["end"]), datetimeFormat).date()
            length = int(streakdata[userid][streakid]["len"])

            cnt_streaks_total += 1
            if cnt_streaks_total % 1000000 == 0:
                logging.info(str(cnt_streaks_total/1000000) + " million streaks computed.")

            if start <= observed_end and end >= observed_start:

                for day in daterange(max(start, observed_start), min(end, observed_end)):

                    badgevalue[userid][str(day)] = ((day - start) + timedelta(days=1)).days

logging.info("Done (2/4)")



logging.info("Computing correlation ... ")

cnt_days = 0

for day in daterange(observed_start, observed_end):

    userval = []
    friendsval = []

    for userid in sampleIDs:

        sum_firends = 0
        cnt_friends = 0 
        for friend in mutual[userid]:
            if friend in badgevalue:
                # only count if mutual connection already exists
                if datetime.datetime.strptime(mutual[userid][friend], datetimeFormat).date() <= day:
                    cnt_friends += 1
                    sum_firends += badgevalue[friend][str(day)]

        if cnt_friends > 0:
            sum_firends /= cnt_friends

            userval.append(badgevalue[userid][str(day)])
            friendsval.append(sum_firends)

    corr[str(day)] = np.corrcoef(userval, friendsval)[0][1]

    cnt_days += 1
    if cnt_days % 100 == 0:
        logging.info(str(cnt_days) + " days computed.")

logging.info("Done (3/4)")



logging.info("Saving ...")
with open(path_results, "w") as fp:
    json.dump(corr, fp)
logging.info("Done (4/4)")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))