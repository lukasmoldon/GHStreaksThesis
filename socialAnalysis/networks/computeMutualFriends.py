# ---------- IMPORT ------------
import logging
import datetime
from datetime import date, timedelta
import json
import pandas as pd
# ------------------------------


# ---------- INPUT -------------
path_source = "/home/johannes/data/github/mysql-2019-06-01/followers.csv"
path_source_userids = "/home/lmoldon/data/users_reduced_IDs.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/data/mutualFriends.json"
# ------------------------------


# ---------- CONFIG ------------
chunksize = 10000000
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d %H:%M:%S"
single_edges = {}
data = {}
changedate = date(2016, 5, 19)
# ------------------------------



log_starttime = datetime.datetime.now()


logging.info("Loading data ...")
with open(path_source_userids, "r") as fp:
    userids = json.load(fp)
logging.info("Done (1/3)")


logging.info("Starting ... ")
cnt = 0
for chunk in pd.read_csv(path_source, chunksize=chunksize, header=None, delimiter=",", names=["user_id", "follower_id", "created_at"]):
    for row in list(chunk.values):
        if str(row[0]) in userids and str(row[1]) in userids:
            try:
                timestamp = datetime.datetime.strptime(str(row[2]), datetimeFormat).date()
                single = False
                if timestamp < changedate:
                    if str(row[0]) in single_edges: # search for 0 ----> 1
                        if str(row[1]) in single_edges[str(row[0])]:
                            del single_edges[str(row[0])][str(row[1])]
                            if str(row[0]) in data:
                                data[str(row[0])].append(str(row[1]))
                            else:
                                data[str(row[0])] = [str(row[1])]
                            if str(row[1]) in data:
                                data[str(row[1])].append(str(row[0]))
                            else:
                                data[str(row[1])] = [str(row[0])]
                        else:
                            single = True
                    else:
                        single = True
                    if single: # add 1 ----> 0
                        if str(row[1]) in single_edges:
                            single_edges[str(row[1])][str(row[0])] = 0 
                        else:
                            single_edges[str(row[1])] = {str(row[0]): 0}
                cnt += 1
                if cnt % 1000000 == 0: logging.info(str(cnt/1000000) + " million edges computed")
            except:
                logging.warning("Could not read the following line:")
                logging.warning(str(row))

cnt_users = 0
cnt_mutuals = 0
for userid in data:
    data[userid] = list(dict.fromkeys(data[userid])) # remove mutual duplicates
    cnt_users += 1
    cnt_mutuals += len(data[userid])
cnt_mutuals = int(cnt_mutuals/2)

logging.info("Done (2/3)")


logging.info("Saving ...")
with open(path_results, "w") as fp:
    json.dump(data, fp)
logging.info("Done (3/3)")

logging.info("Users in set: " + str(cnt_users))
logging.info("Mutual edges in set " + str(cnt_mutuals))

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))