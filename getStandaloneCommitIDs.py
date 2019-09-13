# ---------- IMPORT ------------
import pandas as pd
import logging
import json
# ------------------------------


# ---------- INPUT -------------
path_source_project_commits = "/home/johannes/data/github/mysql-2019-06-01/project_commits.csv"
path_source_project_standaloneIDs = "/home/lmoldon/data/standalone_ProjectIDs.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/data/standalone_CommitIDs.json"
# ------------------------------


# ---------- CONFIG ------------
chunksize = 1000000
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
data = {} # dict for saving commit IDs of standalone projects as keys, value = 0
project_standaloneIDs = set() # temporary store project_standaloneIDs in a set for better performance (membership query is faster on sets)
cnt_analysed = 0
# ------------------------------



logging.info("Reading standalone_ProjectIDs.json, please wait ...")
with open(path_source_project_standaloneIDs, "r") as fp:
    project_standaloneIDs_raw = json.load(fp)

logging.info("Done. (1/3)")


logging.info("Converting IDs to set() ...")
for projectid in project_standaloneIDs_raw:
    project_standaloneIDs.add(projectid)

logging.info("Done. (2/3)")


logging.info("Starting ...")
cnt = 0
for chunk in pd.read_csv(path_source_project_commits, chunksize=chunksize, header=None, delimiter=",", usecols=[0,1], names=["project_id","commit_id"]):
    for row in list(chunk.values):
        cnt_analysed += 1
        if str(row[0]) in project_standaloneIDs:
            data[str(row[1])] = 0


    cnt += 1
    logging.info("Chunk counter = " + str(cnt))


logging.info("Storing data ...")
with open(path_results, "w") as fp:
    json.dump(data, fp)


logging.info("Total commits: 1368240000")
logging.info("Commits analysed " + str(cnt_analysed) + " times.")
logging.info("Commits made in standalone (and also maybe in forked) projects: " + str(len(data)))
logging.info("Commits only made in forked projects: " + str(1368240000-len(data)))
logging.info("Done. (3/3)")