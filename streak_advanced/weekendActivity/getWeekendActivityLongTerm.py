# ---------- IMPORT ------------
import logging
import datetime
import json
from datetime import date, timedelta
# ------------------------------


# ---------- INPUT -------------
path_source = "/home/lmoldon/data/contributions_per_user_per_day.json"
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
observed_start = date(2015, 5, 18) # this must be a monday
observed_end = date(2016, 5, 15) # this must be a sunday
#observed_start = date(2016, 5, 23) # this must be a monday
#observed_end = date(2017, 5, 21) # this must be a sunday
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
weekdata = {}
cnt_users_total = 0
# ------------------------------



def getWeekMonday(strdate):
    date = datetime.datetime.strptime(strdate, datetimeFormat).date()
    monday = date - timedelta(days=date.weekday())
    if monday >= observed_start and monday <= observed_end:
        return monday
    else:
        return -1 # out of observed range (not in weekdata)

def isWeekend(strdate):
    date = datetime.datetime.strptime(strdate, datetimeFormat).date()
    if date.weekday() < 5:
        return False
    else:
        return True


log_starttime = datetime.datetime.now()

logging.info("Loading data ...")
with open(path_source, "r") as fp:
    contributiondata = json.load(fp)
logging.info("Done (1/2)")


logging.info("Starting ...")

i = observed_start
while i < observed_end:
    weekdata[str(i)] = {"WD": 0, "WE": 0, "RW:": 0} # RW: ratio weekend activity
    i += timedelta(days=7)

for userID in contributiondata:

    cnt_users_total += 1
    if cnt_users_total % 10000 == 0:
        logging.info(str(cnt_users_total/1000) + "k users computed.")

    for day in contributiondata[userID]:
        monday = getWeekMonday(day)
        if monday != -1:
            if not isWeekend(day):
                weekdata[str(monday)]["WD"] += contributiondata[userID][day]
            else:
                weekdata[str(monday)]["WE"] += contributiondata[userID][day]

for index in weekdata:
    weekdata[index]["RW"] = weekdata[index]["WE"] / (weekdata[index]["WD"] + weekdata[index]["WE"])

res = 0
for index in weekdata:
    res += weekdata[index]["RW"]
res /= len(weekdata)


logging.info("Done (2/2)")

logging.info("Avg weekend activity: " + str(res))



log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))