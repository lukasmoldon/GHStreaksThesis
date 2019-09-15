# ---------- IMPORT ------------
import logging
import json
import ijson
import datetime
from datetime import timedelta, date
# ------------------------------


# ---------- INPUT -------------
path_source = "/home/lmoldon/data/users_reduced.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/data/usergroupsize.json"
# ------------------------------


# ---------- CONFIG ------------
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d %H:%M:%S"
groupsize = {} # store size of observed usergroup "users_reduced.json" for each day (key = date, value = size of usergroup on that day)
entry_dates = {} # temporary store entry dates of observed usergroup "users_reduced.json" for each day (key = date, value = number of users joined GitHub)
start_date = date(2016, 5, 19)
end_date = date(2016, 5, 19)

def daterange(observedtime_start, observedtime_end):
        for n in range(int((observedtime_end - observedtime_start).days)):
                yield observedtime_start + timedelta(n)
# ------------------------------



log_starttime = datetime.datetime.now()

# Get GitHub entry dates of all observed users and save them per date
logging.info("Accessing userdata ...")
cnt = 0
jsonfile = ijson.parse(open(path_source, "r"))
for prefix, event, value in jsonfile:
    if ".created_at" in prefix: # prefix = userid.created_at, value = date
        cnt += 1
        if cnt % 100000 == 0:
            logging.info(str(cnt) + " users computed.")

        day = datetime.datetime.strptime(str(value), datetimeFormat).date()
        if day > end_date:
            end_date = day
        if day < start_date:
            start_date = day

        day = str(day)
        if day in entry_dates:
            entry_dates[day] += 1
        else:
            entry_dates[day] = 1
        
logging.info("Done. (1/2)")


# Calculate size of usergroup per day in interval [start_date, end_date]
logging.info("Calculating size of usergroup per day...")
cnt = 0
for single_date in daterange(start_date, end_date):
    groupsize[str(single_date)] = 0

for single_date in daterange(start_date, end_date):
    if str(single_date) in entry_dates:
        for following_date in daterange(single_date, end_date):
            groupsize[str(following_date)] += entry_dates[str(single_date)]
    else:
        logging.warning("No users of observed group joined on " + str(single_date))
    cnt += 1
    if cnt % 100 == 0:
        logging.info("Days computed: " + str(cnt))
    


logging.info("Storing data ...")
with open(path_results, "w") as fp:
    json.dump(groupsize, fp)

logging.info("Start date: " + str(start_date))
logging.info("End date: " + str(end_date))
logging.info("Total amount of days in range: " + str(cnt))
logging.info("Done. (2/2)")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))