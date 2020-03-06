# ---------- IMPORT ------------
import logging
import datetime
from datetime import date, timedelta
import json
import pandas as pd
# ------------------------------


# ---------- INPUT -------------
path_source = "/home/johannes/data/github/mysql-2019-06-01/followers.csv"
path_source_mutual = "/home/lmoldon/data/mutualFriends.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/data/mutualFriendsStarting.json"
# ------------------------------


# ---------- CONFIG ------------
chunksize = 10000000
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d %H:%M:%S"
data = {}
# ------------------------------



log_starttime = datetime.datetime.now()


logging.info("Loading data ...")
with open(path_source_mutual, "r") as fp:
    mutual = json.load(fp)
logging.info("Done (1/3)")


logging.info("Starting ... ")
cnt = 0
for chunk in pd.read_csv(path_source, chunksize=chunksize, header=None, delimiter=",", names=["user_id", "follower_id", "created_at"]):
    for row in list(chunk.values):
        if str(row[0]) in mutual and str(row[1]) in mutual:
            timestamp = datetime.datetime.strptime(str(row[2]), datetimeFormat).date()
            cnt += 1
            if cnt % 1000000 == 0: logging.info(str(cnt/1000000) + " million edges computed")

            if str(row[0]) in data:
                if str(row[1]) in data[str(row[0])]:
                    data[str(row[0])][str(row[1])] = str(max(datetime.datetime.strptime(data[str(row[0])][str(row[1])], "%Y-%m-%d").date(), timestamp))
                else:
                    data[str(row[0])][str(row[1])] = str(timestamp)
            else:
                data[str(row[0])] = {str(row[1]): str(timestamp)}

            if str(row[1]) in data:
                if str(row[0]) in data[str(row[1])]:
                    data[str(row[1])][str(row[0])] = str(max(datetime.datetime.strptime(data[str(row[1])][str(row[0])], "%Y-%m-%d").date(), timestamp))
                else:
                    data[str(row[1])][str(row[0])] = str(timestamp)
            else:
                data[str(row[1])] = {str(row[0]): str(timestamp)}

logging.info("Done (2/3)")


logging.info("Saving ...")
with open(path_results, "w") as fp:
    json.dump(data, fp)
logging.info("Done (3/3)")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))