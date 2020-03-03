# ---------- IMPORT ------------
import pandas as pd
import logging
import datetime
import json
import sys
# ------------------------------


# ---------- INPUT -------------
path_source_issues = "/home/johannes/data/github/mysql-2019-06-01/issues.csv"

try:
    userID = sys.argv[1]
except:
    logging.critical("Wrong usage: No valid userID provided as first argument!")
    sys.exit()
# ------------------------------


# ---------- OUTPUT ------------
path_results = "..."
# ------------------------------


# ---------- CONFIG ------------
chunksize = 1000000
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
issuedata = {} 
path_results = "/home/lmoldon/results/verification/issues_" + userID + ".json"
# ------------------------------



log_starttime = datetime.datetime.now()



# store issuedata for all issues with issuer_ids in users_reduced_IDs.json
logging.info("Accessing issuedata ...")
cnt = 0
for chunk in pd.read_csv(path_source_issues, chunksize=chunksize, header=None, delimiter=",", usecols=[0,1,2,6], names=["id","repo_id","reporter_id","created_at"]):
    for row in list(chunk.values):
        if str(row[2]) == userID:
            issuedata[str(row[3])] = 0
    cnt += 1
    logging.info("Chunk counter = " + str(cnt))


logging.info("Storing data ... ")
with open(path_results, "w") as fp:
    json.dump(issuedata, fp)

logging.info("Done.")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))