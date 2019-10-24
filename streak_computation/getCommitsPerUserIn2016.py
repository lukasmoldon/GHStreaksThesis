# ---------- IMPORT ------------
import pandas as pd
import logging
import datetime
import json
import ijson
# ------------------------------


# ---------- INPUT -------------
path_source_commits = "/home/johannes/data/github/mysql-2019-06-01/commits.csv"
path_source_standalonecommitids = "/home/lmoldon/data/standalone_CommitIDs.json" 
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/data/commits_per_user_2016.json"
# ------------------------------


# ---------- CONFIG ------------
chunksize = 1000000
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d %H:%M:%S"
data = {} # dict for saving IDs as keys and amount of commits as value
standalonecommitids = set() # temporary store sommit_standaloneIDs in a set for better performance (membership query is faster on sets)
year_start = datetime.datetime.strptime("2016-01-01 00:00:01", datetimeFormat)
year_end = datetime.datetime.strptime("2016-12-31 23:59:59", datetimeFormat)
# ------------------------------



log_starttime = datetime.datetime.now()

logging.info("Converting standalone_CommitIDs to set() ...")
cnt = 0
jsonfile = ijson.parse(open(path_source_standalonecommitids, "r"))
for prefix, event, value in jsonfile:
    if event == "number":
        standalonecommitids.add(str(prefix))
        cnt += 1
        if cnt % 1000000 == 0:
            logging.info(str(cnt/1000000) + " million commits in set()")

logging.info("Done. (1/2)")


logging.info("Starting ...")
cnt = 0
for chunk in pd.read_csv(path_source_commits, chunksize=chunksize, header=None, delimiter=",", usecols=[0,3,5], names=["id","committer_id","created_at"]):
    for row in list(chunk.values):
        timestamp = datetime.datetime.strptime(str(row[2]), datetimeFormat)
        if timestamp > year_start and timestamp < year_end:
            commitid = str(row[0])
            if commitid in standalonecommitids:
                userid = str(row[1])
                if userid in data:
                    data[userid] += 1
                else:
                    data[userid] = 1
    cnt += 1
    logging.info("Chunk counter = " + str(cnt))


logging.info("Storing data ...")
with open(path_results, "w") as fp:
    json.dump(data, fp)

logging.info("Done. (2/2)")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))