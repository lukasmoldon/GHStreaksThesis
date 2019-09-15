# ---------- IMPORT ------------
import pandas as pd
import logging
import json
import datetime
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
startinterval = datetime.datetime.strptime("2011-01-01 00:00:01", datetimeFormat)
endinterval = datetime.datetime.strptime("2019-04-01 23:59:59", datetimeFormat) 
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
data = {} # key = date between start and end, value = amount of commits at that day 
# ------------------------------



log_starttime = datetime.datetime.now()

logging.info("Starting ...")
cnt = 0
for chunk in pd.read_csv(path_source, chunksize=chunksize, header=None, delimiter=",", usecols=[3], names=["created_at"]):
    for timestamp in list(chunk["created_at"].values):
        try:
            date = datetime.datetime.strptime(timestamp, datetimeFormat)
            if date >= startinterval and date <= endinterval:
                day = str(date.date())
                if day in data:
                    data[day] += 1
                else:
                    data[day] = 1
        except:
            logging.warning("Saving Date failed at chunk " + str(cnt+1))
    cnt += 1
    logging.info("Chunk counter = " + str(cnt))


logging.info("Storing data ... ")
with open(path_results, "w") as fp:
    json.dump(data, fp)

logging.info("Done.")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))