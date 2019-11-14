# ---------- IMPORT ------------
import logging
import datetime
from datetime import timedelta, date
import json
import pandas as pd
import random
# ------------------------------


# ---------- INPUT -------------
path_source_streakdata = "/home/lmoldon/data/user_streaks.json"
path_source_dates_per_user = "/home/lmoldon/data/contributions_per_user_per_day.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/results/regressionData.csv"
# ------------------------------


# ---------- CONFIG ------------
datetimeFormat = "%Y-%m-%d"
observed_start = datetime.datetime.strptime("2015-05-19", datetimeFormat).date() # start of observed time, 1 year before the change
observed_end = datetime.datetime.strptime("2017-05-20", datetimeFormat).date() # end of observed time, 1 year after the change
minLength = 1 # minimum streak length for observations
user_sample_size = 10000
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
changeDate = datetime.datetime.strptime("2016-05-19", datetimeFormat).date()
data = pd.DataFrame(columns=["userday", "after_change", "current_streak", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"])
row = {
    "userday": "",
    "after_change": 0,
    "current_streak": 0,
    "monday": 0,
    "tuesday": 0,
    "wednesday": 0,
    "thursday": 0,
    "friday": 0,
    "saturday": 0,
    "sunday": 0
    }
cnt_streaks_total = 0
cnt_streaks_observed = 0
cnt_users = 0
user_sample = {} # key = userID, value = 0 (ignore)
userIDs = []
# ------------------------------



def daterange(observedtime_start, observedtime_end):
        for n in range(int((observedtime_end - observedtime_start).days + 1)):
                yield observedtime_start + timedelta(n)



log_starttime = datetime.datetime.now()


logging.info("Loading data ...")
with open(path_source_streakdata, "r") as fp:
    streakdata = json.load(fp)

with open(path_source_dates_per_user, "r") as fp:
    contributiondata = json.load(fp)
logging.info("Done. (1/5)")


logging.info("Creating user sample ...")

userIDs = list(streakdata)

while len(user_sample) != 10000:
    cur_userid = random.choice(userIDs)
    if cur_userid not in user_sample:
        if cur_userid in contributiondata:
            user_sample[cur_userid] = 0
        else:
            logging.info("UserID " + str(cur_userid) + " has an entry in the streakdata but not in the contributiondata!")

logging.info("Done. (2/5)")


logging.info("Computing streak data ...")
# for all days where current_streak != 0
for userid in user_sample: # for each user in sample
    for streakid in streakdata[userid]: # for each streak of that user

        start = datetime.datetime.strptime(str(streakdata[userid][streakid]["start"]), datetimeFormat).date()
        end = datetime.datetime.strptime(str(streakdata[userid][streakid]["end"]), datetimeFormat).date()
        length = int(streakdata[userid][streakid]["len"])
            
        cnt_streaks_total += 1
        if cnt_streaks_total % 1000 == 0:
            logging.info(str(cnt_streaks_total/1000) + " thousand streaks computed.")

        if length >= minLength and start <= observed_end and end >= observed_start: # streak happend (partially) in observed time
            cnt_streaks_observed += 1

            if start >= observed_start: # start in observed time
                if end < observed_end: # start and end in observed time
                    for single_date in daterange(start, end):
                        cur_row = row
                        cur_row["userday"] = str(userid) + "_" + str(single_date)
                        if single_date >= changeDate:
                            cur_row["after_change"] = 1
                        cur_row["current_streak"] = ((single_date - start) + timedelta(days=1)).days
                        cur_row[str(single_date.strftime("%A").lower())] = 1
                        data = data.append(row, ignore_index=True)
                else: # start in observed time, end not in observed time
                    for single_date in daterange(start, observed_end):
                        cur_row = row
                        cur_row["userday"] = str(userid) + "_" + str(single_date)
                        if single_date >= changeDate:
                            cur_row["after_change"] = 1
                        cur_row["current_streak"] = ((single_date - start) + timedelta(days=1)).days
                        cur_row[str(single_date.strftime("%A").lower())] = 1
                        data = data.append(row, ignore_index=True)
            else: # start not in observed time
                if end < observed_end: # start not in observed time, but end in observed time
                    for single_date in daterange(observed_start, end):
                        cur_row = row
                        cur_row["userday"] = str(userid) + "_" + str(single_date)
                        if single_date >= changeDate:
                            cur_row["after_change"] = 1
                        cur_row["current_streak"] = ((single_date - start) + timedelta(days=1)).days
                        cur_row[str(single_date.strftime("%A").lower())] = 1
                        data = data.append(row, ignore_index=True)
                else: # start and end not in observed time
                    for single_date in daterange(observed_start, observed_end):
                        cur_row = row
                        cur_row["userday"] = str(userid) + "_" + str(single_date)
                        if single_date >= changeDate:
                            cur_row["after_change"] = 1
                        cur_row["current_streak"] = ((single_date - start) + timedelta(days=1)).days
                        cur_row[str(single_date.strftime("%A").lower())] = 1
                        data = data.append(row, ignore_index=True)

logging.info("Done. (3/5)")


logging.info("Computing contribution data ...")
# for all days where current_streak == 0
for userid in user_sample:
    cnt_users += 1
    if cnt_users % 100 == 0:
        logging.info(str(cnt_users) + " users computed.")
    for single_date in daterange(observed_start, observed_end):
        if str(single_date) not in contributiondata[userid]:
            cur_row = row
            cur_row["userday"] = str(userid) + "_" + str(single_date)
            if single_date >= changeDate:
                cur_row["after_change"] = 1
            cur_row["current_streak"] = 0
            cur_row[str(single_date.strftime("%A").lower())] = 1
            data = data.append(row, ignore_index=True)

logging.info("Done. (4/5)")


logging.info("Saving csv ...")
data.to_csv(path_results, encoding='utf-8', index=False)
logging.info("Done. (5/5)")


logging.info("Streaks total: " + str(cnt_streaks_total))
logging.info("Streaks observed: " + str(cnt_streaks_observed))


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))