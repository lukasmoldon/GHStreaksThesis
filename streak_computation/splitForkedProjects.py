# ---------- IMPORT ------------
import pandas as pd
import logging
import datetime
import json
# ------------------------------


# ---------- INPUT -------------
path_source = "/home/johannes/data/github/mysql-2019-06-01/projects.csv"
# ------------------------------


# ---------- OUTPUT ------------
path_results_forked = "/home/lmoldon/data/forked_ProjectIDs.json"
path_results_standalone = "/home/lmoldon/data/standalone_ProjectIDs.json"
# ------------------------------


# ---------- CONFIG ------------
chunksize = 1000000
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
forkedProjectIDs = {} # store IDs of forked projects (key = projectID, value = 0)
standaloneProjectIDs = {} # store IDs of standalone projects (key = projectID, value = 0)
cnt_projects_total = 0
cnt_projects_forked = 0
# ------------------------------



log_starttime = datetime.datetime.now()

logging.info("Accessing project data ...")
cnt = 0
for chunk in pd.read_csv(path_source, chunksize=chunksize, header=None, delimiter=",", usecols=[0,7], names=["id","forked_from"]):
    for row in list(chunk.values):
        cnt_projects_total += 1
        if str(row[1]) != "\\N" and str(row[1]) != "0":
            cnt_projects_forked += 1
            forkedProjectIDs[str(row[0])] = 0
        else:
            standaloneProjectIDs[str(row[0])] = 0
    cnt += 1
    logging.info("Chunk counter = " + str(cnt))


logging.info("Storing data ... (1/2)")
with open(path_results_forked, "w") as fp:
    json.dump(forkedProjectIDs, fp)

logging.info("Storing data ... (2/2)")
with open(path_results_standalone, "w") as fp:
    json.dump(standaloneProjectIDs, fp)

logging.info("Total number of projects: " + str(cnt_projects_total))
logging.info("Number of forked projects: " + str(cnt_projects_forked) + " (" + str((cnt_projects_forked/cnt_projects_total)*100) + "%)")
logging.info("Done.")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))