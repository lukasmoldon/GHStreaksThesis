# ---------- IMPORT ------------
import pandas as pd
import logging
import json
import datetime
from datetime import timedelta, date
# ------------------------------


# ---------- INPUT -------------
path_source = "/home/johannes/data/github/mysql-2019-06-01/users.csv"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/data/communitysize_per_day.json"
# ------------------------------


# ---------- CONFIG ------------
chunksize = 100000
datetimeFormat = "%Y-%m-%d %H:%M:%S"
startinterval = date(2011, 1, 1)
endinterval = date(2019, 4, 1)
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
data = {} # key = date between start and end, value = amount of commits at that day 
communitysize = {}
# ------------------------------


def daterange(observedtime_start, observedtime_end):
        for n in range(int((observedtime_end - observedtime_start).days)):
                yield observedtime_start + timedelta(n)



log_starttime = datetime.datetime.now()

logging.info("Starting ...")
cnt = 0
for chunk in pd.read_csv(path_source, chunksize=chunksize, header=None, delimiter=",", usecols=[3], names=["created_at"]):
    for timestamp in list(chunk["created_at"].values):
        try:
            date = datetime.datetime.strptime(timestamp, datetimeFormat).date()
            if date >= startinterval and date <= endinterval:
                date = str(date)
                if date in data:
                    data[date] += 1
                else:
                    data[date] = 1
        except:
            logging.warning("Saving Date failed at chunk " + str(cnt+1))
    cnt += 1
    logging.info("Chunk counter = " + str(cnt))

logging.info("Done (1/3)")


# Calculate size of community per day in interval [startinterval, endinterval]
logging.info("Calculating size of community per day...")
cnt = 0
for single_date in daterange(startinterval, endinterval):
    communitysize[str(single_date)] = 0

for single_date in daterange(startinterval, endinterval):
    if str(single_date) in data:
        for following_date in daterange(single_date, endinterval):
            communitysize[str(following_date)] += data[str(single_date)]
    else:
        logging.warning("No users of observed group joined on " + str(single_date))
    cnt += 1
    if cnt % 100 == 0:
        logging.info("Days computed: " + str(cnt))
    
logging.info("Done (2/3)")


logging.info("Storing data ... ")
with open(path_results, "w") as fp:
    json.dump(communitysize, fp)

logging.info("Done. (3/3)")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))