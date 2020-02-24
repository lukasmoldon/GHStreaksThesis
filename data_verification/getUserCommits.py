# ---------- IMPORT ------------
import pandas as pd
import logging
import datetime
import json
# ------------------------------


# ---------- INPUT -------------
path_source_commits = "/home/johannes/data/github/mysql-2019-06-01/commits.csv"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/scripts/dates.json"
# ------------------------------


# ---------- CONFIG ------------
chunksize = 1000000
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
data = {} # dict for saving IDs as keys and amount of commits as value
# ------------------------------



log_starttime = datetime.datetime.now()


logging.info("Starting ...")
cnt = 0
for chunk in pd.read_csv(path_source_commits, chunksize=chunksize, header=None, delimiter=",", usecols=[0,3,4,5], names=["id","committer_id","project_id","created_at"]):
    for row in list(chunk.values):
        if str(row[1]) == "10891816":
            if str(row[3]) in data:
                data[str(row[3])] += 1
            else:
                data[str(row[3])] = 1
    cnt += 1
    logging.info("Chunk counter = " + str(cnt))


logging.info("Storing data ...")
with open(path_results, "w") as fp:
    json.dump(data, fp)

logging.info("Done.")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))