# ---------- IMPORT ------------
import logging
import datetime
import json
from datetime import timedelta, date
# ------------------------------


# ---------- INPUT -------------
path_source_streakdata = "/home/lmoldon/data/user_streaks.json"
path_source_userdata = "/home/lmoldon/data/users_reduced.json"
path_source_genderdata = "/home/lmoldon/data/users_gender.json"
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
threshold = 20
observed_start = date(2013, 1, 1)
changedate = date(2016,5,19)
observed_end = date(2019, 4, 1)
# ------------------------------


# ---------- INITIAL -----------
datetimeFormat = "%Y-%m-%d"
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
data_before = {
    "male": {},
    "female": {}
}
data_after = {
    "male": {},
    "female": {}
}
# ------------------------------



def daterange(observedtime_start, observedtime_end):
        for n in range(int((observedtime_end - observedtime_start).days + 1)):
                yield observedtime_start + timedelta(n)



log_starttime = datetime.datetime.now()

logging.info("Loading data ...")
with open(path_source_streakdata, "r") as fp:
    streakdata = json.load(fp)

with open(path_source_userdata, "r") as fp:
    userids = json.load(fp)

with open(path_source_genderdata, "r") as fp:
    genderdata = json.load(fp)

logging.info("Done (1/2)")


deleteIDs = set()
for userid in userids:
    if userid not in streakdata:
        deleteIDs.add(userid)
    elif userid not in genderdata:
        deleteIDs.add(userid)
    elif genderdata[userid]["gender"] != "male" and genderdata[userid]["gender"] != "female":
        deleteIDs.add(userid)

for userid in deleteIDs:
    del userids[userid]


logging.info("Starting ... ")

cnt_streaks_total = 0
for userid in userids:

    for streakid in streakdata[userid]:

        start = datetime.datetime.strptime(str(streakdata[userid][streakid]["start"]), datetimeFormat).date()
        end = datetime.datetime.strptime(str(streakdata[userid][streakid]["end"]), datetimeFormat).date()
        length = int(streakdata[userid][streakid]["len"])
        gender = genderdata[userid]["gender"]

        cnt_streaks_total += 1
        if cnt_streaks_total % 1000000 == 0:
            logging.info(str(cnt_streaks_total/1000000) + " million streaks computed.")

        if start >= observed_start and start <= changedate:
            if userid in data_before[gender]:
                data_before[gender][userid] = max(data_before[gender][userid], length)
            else:
                data_before[gender][userid] = length
        elif start >= changedate and start <= observed_end:
            if userid in data_after[gender]:
                data_after[gender][userid] = max(data_after[gender][userid], length)
            else:
                data_after[gender][userid] =  length

male_before = 0
male_after = 0
female_before = 0
female_after = 0

for userid in data_before["male"]:
    if data_before["male"][userid] >= threshold:
        male_before += 1
male_before = male_before / len(data_before["male"])

for userid in data_after["male"]:
    if data_after["male"][userid] >= threshold:
        male_after += 1
male_after = male_after / len(data_after["male"])

for userid in data_before["female"]:
    if data_before["female"][userid] >= threshold:
        female_before += 1
female_before = female_before / len(data_before["female"])

for userid in data_after["female"]:
    if data_after["female"][userid] >= threshold:
        female_after += 1
female_after = female_after / len(data_after["female"])

logging.info("Done (2/2)")

logging.info("MALE >= 20 before: " + str(male_before))
logging.info("MALE >= 20 after: " + str(male_after))
logging.info("FEMALE >= 20 before: " + str(female_before))
logging.info("FEMALE >= 20 after: " + str(female_after))

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))