# ---------- IMPORT ------------
import pandas as pd
import logging
import datetime
import json
import ijson
# ------------------------------


# ---------- INPUT -------------
path_source_language = "/home/johannes/data/github/mysql-2019-06-01/project_languages.csv"
path_source_standaloneIDs = "/home/lmoldon/data/standalone_ProjectIDs.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results_language = "/home/lmoldon/data/project_languages_reduced.json"
path_results_stats = "/home/lmoldon/results/project_languages_distribution.json"
# ------------------------------


# ---------- CONFIG ------------
chunksize = 1000000
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
cnt_projects = 0
cnt_langauges = {} # key = langauge name, value = count
result_langauges = {}
# ------------------------------



log_starttime = datetime.datetime.now()


logging.info("Loading data ...")
with open(path_source_standaloneIDs, "r") as fp:
    standaloneIDs = json.load(fp)
logging.info("Done. (1/2)")


logging.info("Accessing language data ...")
cnt = 0
for chunk in pd.read_csv(path_source_language, chunksize=chunksize, header=None, delimiter=",", names=["project_id", "language", "bytes", "created_at"]):
    for row in list(chunk.values):
        if str(row[0]) in standaloneIDs:
            cnt_projects += 1
            result_langauges[str(row[0])] = str(row[1])
            if str(row[1]) in cnt_langauges:
                cnt_langauges[str(row[1])] += 1
            else:
                cnt_langauges[str(row[1])] = 1
    cnt += 1
    logging.info("Chunk counter = " + str(cnt))


logging.info("Storing data ... (1/2)")

with open(path_results_language, "w") as fp:
    json.dump(result_langauges, fp)

logging.info("Storing data ... (2/2)")

stats_final = dict({c: v for c, v in sorted(cnt_langauges.items(), key=lambda item: item[1])})

with open(path_results_stats, "w") as fp:
    json.dump(stats_final, fp)

logging.info("Total surviving projects: " + str(cnt_projects))
logging.info("Done. (2/2)")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))