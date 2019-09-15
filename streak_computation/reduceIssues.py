# ---------- IMPORT ------------
import pandas as pd
import logging
import datetime
import json
# ------------------------------


# ---------- INPUT -------------
path_source_issues = "/home/johannes/data/github/mysql-2019-06-01/issues.csv"
path_source_userids = "/home/lmoldon/data/users_reduced_IDs.json"
path_source_project_standaloneIDs = "/home/lmoldon/data/standalone_ProjectIDs.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/data/issues_reduced.json"
# ------------------------------


# ---------- CONFIG ------------
chunksize = 1000000
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
issuedata = {} # store issuedata (key = issueid, value = issuedata)
ids = set() # temporary store userids of observed usergroup "users_reduced_IDs.json" in a set for better performance (membership query is faster on sets)
project_standaloneIDs = set() # temporary store project_standaloneIDs in a set for better performance (membership query is faster on sets)
cnt_issues = 0
# ------------------------------



log_starttime = datetime.datetime.now()

logging.info("Converting userIDs to set() ...")
with open(path_source_userids, "r") as fp:
    users_reduced_IDs = json.load(fp)

for el in users_reduced_IDs:
    ids.add(el)
logging.info("Done. (1/4)")


logging.info("Reading standalone_ProjectIDs.json, please wait ...")
with open(path_source_project_standaloneIDs, "r") as fp:
    project_standaloneIDs_raw = json.load(fp)

logging.info("Done. (2/4)")


logging.info("Converting ProjectIDs to set() ...")
for projectid in project_standaloneIDs_raw:
    project_standaloneIDs.add(projectid)

logging.info("Done. (3/4)")


# store issuedata for all issues with issuer_ids in users_reduced_IDs.json
logging.info("Accessing issuedata ...")
cnt = 0
for chunk in pd.read_csv(path_source_issues, chunksize=chunksize, header=None, delimiter=",", usecols=[0,1,2,6], names=["id","repo_id","reporter_id","created_at"]):
    for row in list(chunk.values):
        if str(row[2]) in ids:
            if str(row[1]) in project_standaloneIDs:
                cnt_issues += 1
                issuedata[str(row[0])] = {
                    "project_id": row[1],
                    "user_id": row[2],
                    "created_at": row[3]
                }
    cnt += 1
    logging.info("Chunk counter = " + str(cnt))


logging.info("Storing data ... ")
with open(path_results, "w") as fp:
    json.dump(issuedata, fp)

logging.info("Total issues survived: " + str(cnt_issues))
logging.info("Done. (4/4)")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))