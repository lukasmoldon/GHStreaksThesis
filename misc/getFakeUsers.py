# ---------- IMPORT ------------
import pandas as pd
import logging
import datetime
import json
# ------------------------------


# ---------- INPUT -------------
path_source_userdata = "/home/johannes/data/github/mysql-2019-06-01/users.csv"
path_source_commits = "/home/johannes/data/github/mysql-2019-06-01/commits.csv"
# ------------------------------


# ---------- OUTPUT ------------
path_results_fakeids = "/home/lmoldon/data/fakeuser_IDs.json"
# ------------------------------


# ---------- CONFIG ------------
chunksize = 1000000
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
cnt_users = 0
cnt_commits = 0
cnt_fake_users = 0
cnt_fake_commits = 0
fakeuserids = {}
# ------------------------------



log_starttime = datetime.datetime.now()

logging.info("Accessing userdata ...")
cnt = 0
for chunk in pd.read_csv(path_source_userdata, chunksize=chunksize, header=None, delimiter=",", usecols=[0,5], names=["id","fake"]):
    for row in list(chunk.values):
        cnt_users += 1
        if str(row[1]) == "1":
            fakeuserids[str(row[0])] = 0
            cnt_fake_users += 1
    cnt += 1
    logging.info("Chunk counter = " + str(cnt))


logging.info("Storing fake userIDs ... ")
with open(path_results_fakeids, "w") as fp:
    json.dump(fakeuserids, fp)

logging.info("Done. (1/2)")



logging.info("Accessing commitdata ...")
cnt = 0
for chunk in pd.read_csv(path_source_commits, chunksize=chunksize, header=None, delimiter=",", usecols=[3], names=["committer_id"]):
    for row in list(chunk.values):
        cnt_commits += 1
        if str(row[0]) in fakeuserids:
            cnt_fake_commits += 1
    cnt += 1
    logging.info("Chunk counter = " + str(cnt))

logging.info("Done. (2/2)")

logging.info("------------------------------")
logging.info("Total users: " + str(cnt_users))
logging.info("Fake users: " + str(cnt_fake_users))
logging.info("Share fake: " + str((cnt_fake_users/cnt_users)*100))
logging.info("------------------------------")
logging.info("Total commits: " + str(cnt_commits))
logging.info("Commits by fake users: " + str(cnt_fake_commits))
logging.info("Share fake commits by fake users: " + str((cnt_fake_commits/cnt_commits)*100))
logging.info("------------------------------")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))