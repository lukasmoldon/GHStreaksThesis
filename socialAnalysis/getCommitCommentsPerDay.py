# ---------- IMPORT ------------
import logging
import datetime
import json
import datetime
from datetime import timedelta, date
import pandas as pd

import time
# ------------------------------


# ---------- INPUT -------------
path_source = "/home/lmoldon/data/commit_comments_repaired.csv"
path_source_userids = "/home/lmoldon/data/users_reduced_IDs.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/results/commitCommentsCount.json"
# ------------------------------


# ---------- CONFIG ------------
chunksize = 1000000
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d %H:%M:%S"
data = {}
# ------------------------------


log_starttime = datetime.datetime.now()


logging.info("Loading data ...")
with open(path_source_userids, "r") as fp:
    userids = json.load(fp)

cnt = 0
for chunk in pd.read_csv(path_source, chunksize=chunksize, header=None, delimiter=",", encoding='utf-8'):
    for row in list(chunk.values):
        if str(row[2]) in userids:
            try:
                timestamp = datetime.datetime.strptime(str(row[7]), datetimeFormat).date()
                cnt += 1
                if cnt % 1000000 == 0: logging.info(str(cnt/1000000) + " million comments computed")
                if str(timestamp) in data:
                    data[str(timestamp)] += 1
                else:
                    data[str(timestamp)] = 1
            except:
                logging.warning("Could not read following line:")
                logging.warning(str(row))
logging.info("Done (1/2)")


logging.info("Saving ...")
with open(path_results, "w") as fp:
    json.dump(data, fp)
logging.info("Done (2/2)")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))