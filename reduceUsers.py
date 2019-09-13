# ---------- IMPORT ------------
import pandas as pd
import logging
import json
import ijson
# ------------------------------


# ---------- INPUT -------------
path_source_userdata = "/home/johannes/data/github/mysql-2019-06-01/users.csv"
path_source_commitsperuser = "/home/lmoldon/data/commits_per_user.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results_userdata = "/home/lmoldon/data/users_reduced.json"
path_results_ids = "/home/lmoldon/data/users_reduced_IDs.json"
# ------------------------------


# ---------- CONFIG ------------
threshold = 100 # minimum amount of commits per user to "survive" in users_reduced group
chunksize = 100000
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
survivors = set() # temporary store userIDs with at least <threshold> commits (lifetime)
userdata = {} # store userdata (key = userid, value = userdata)
users_reduced_ids = {} # store userIDs of users in userdata for faster access (key = userid, value = 0)
cnt_usr = 0
# ------------------------------



# Get userIDs with at least <threshold> commits:
logging.info("Getting users with at least " + str(threshold) + " commits ...")
cnt = 0
jsonfile = ijson.parse(open(path_source_commitsperuser, "r"))
for prefix, event, value in jsonfile:
    if event == "number": # => prefix = userid, value = number of commits
        cnt += 1
        if value >= threshold:
            survivors.add(str(prefix))
        if cnt % 1000000 == 0:
            logging.info(str(cnt/1000000) + " million users computed.")

logging.info("Done. (1/2)")

# For all userIDs in survivors, store userdata and userIDs if not fake, location available and type is USR:
logging.info("Accessing userdata ...")
cnt = 0
for chunk in pd.read_csv(path_source_userdata, chunksize=chunksize, header=None, delimiter=",", usecols=[0,1,3,4,5,6,7,8], names=["id","name","created_at","type","fake","deleted","long","lat"]):
    for row in list(chunk.values):
        if row[3] == "USR" and row[4] == 0 and row[6] != row[7]:
            if str(row[0]) in survivors:
                cnt_usr += 1
                users_reduced_ids[str(row[0])] = 0
                userdata[str(row[0])] = {
                    "name": row[1],
                    "created_at": row[2],
                    "deleted": row[5],
                    "long": row[6],
                    "lat": row[7]
                }
    cnt += 1
    logging.info("Chunk counter = " + str(cnt))


logging.info("Storing data ... (1/2)")
with open(path_results_userdata, "w") as fp:
    json.dump(userdata, fp)

logging.info("Storing data ... (2/2)")
with open(path_results_ids, "w") as fp:
    json.dump(users_reduced_ids, fp)

logging.info("Total users in users_reduced.json: " + str(cnt_usr))
logging.info("Done. (2/2)")