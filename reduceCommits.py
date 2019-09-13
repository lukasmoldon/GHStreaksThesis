# ---------- IMPORT ------------
import pandas as pd
import logging
import json
import ijson
# ------------------------------


# ---------- INPUT -------------
path_source_commits = "/home/johannes/data/github/mysql-2019-06-01/commits.csv"
path_source_userids = "/home/lmoldon/data/users_reduced_IDs.json"
path_source_standalonecommitids = "/home/lmoldon/data/standalone_CommitIDs.json" 
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/data/commits_reduced.json"
# ------------------------------


# ---------- CONFIG ------------
chunksize = 1000000
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
commitdata = {} # store commitdata (key = commitid, value = commitdata)
ids = set() # temporary store userids of observed usergroup "users_reduced_IDs.json" in a set for better performance (membership query is faster on sets)
cnt_commits = 0
standalonecommitids = set() # temporary store sommit_standaloneIDs in a set for better performance (membership query is faster on sets)
# ------------------------------



logging.info("Converting userIDs to set() ...")
with open(path_source_userids, "r") as fp:
    users_reduced_IDs = json.load(fp)

for el in users_reduced_IDs:
    ids.add(el)
logging.info("Done. (1/3)")


logging.info("Converting standalone_CommitIDs to set() ...")
cnt = 0
jsonfile = ijson.parse(open(path_source_standalonecommitids, "r"))
for prefix, event, value in jsonfile:
    if event == "number":
        standalonecommitids.add(str(prefix))
        cnt += 1
        if cnt % 1000000 == 0:
            logging.info(str(cnt/1000000) + " million commits in set()")

logging.info("Done. (2/3)")


# store commitdata for all commits with committer_ids in users_reduced_IDs.json
logging.info("Accessing commit data ...")
cnt = 0
for chunk in pd.read_csv(path_source_commits, chunksize=chunksize, header=None, delimiter=",", usecols=[0,3,4,5], names=["id","committer_id","project_id","created_at"]):
    for row in list(chunk.values):
        if str(row[1]) in ids:
            if str(row[0]) in standalonecommitids:
                cnt_commits += 1
                commitdata[str(row[0])] = {
                    "committer_id": row[1],
                    "project_id": row[2],
                    "created_at": row[3]
                }
    cnt += 1
    logging.info("Chunk counter = " + str(cnt))


logging.info("Storing data ... ")
with open(path_results, "w") as fp:
    json.dump(commitdata, fp)

logging.info("Total commits survived: " + str(cnt_commits))
logging.info("Done. (3/3)")