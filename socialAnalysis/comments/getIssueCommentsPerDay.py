# ---------- IMPORT ------------
import logging
import datetime
import json
import datetime
from datetime import timedelta, date
import pandas as pd

import time
# ------------------------------


# ---------- INPUT -------------
path_source = "/home/johannes/data/github/mysql-2019-06-01/issue_comments.csv"
path_source_userids = "/home/lmoldon/data/users_reduced_IDs.json"
path_source_gender = "/home/lmoldon/data/users_gender.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/results/issueCommentsCount.json"
# ------------------------------


# ---------- CONFIG ------------
chunksize = 1000000
country_restricted = False # True == only count users from country_restrictions
country_restrictions = ["United Kingdom"]
usertype_restricted = False # True == only count users from usertype_restriction
usertype_restriction = "/home/lmoldon/results/nonStreakingUsersMAX5.json"
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d %H:%M:%S"
data = {}
# ------------------------------


log_starttime = datetime.datetime.now()


logging.info("Loading data ...")
with open(path_source_userids, "r") as fp:
    userids = json.load(fp)

with open(path_source_gender, "r") as fp:
    genderdata = json.load(fp)

if country_restricted:
    delIDs = set()
    for userid in userids:
        if userid not in genderdata:
            delIDs.add(userid)
    for userid in delIDs:
        del userids[userid]

if usertype_restricted:
    with open(usertype_restriction, "r") as fp:
        usertypeids = json.load(fp)
    delIDs = set()
    for userid in userids:
        if userid not in usertypeids:
            delIDs.add(userid)
    for userid in delIDs:
        del userids[userid]

logging.info("Done (1/3)")


logging.info("Starting ...")
cnt = 0
for chunk in pd.read_csv(path_source, chunksize=chunksize, header=None, delimiter=",", encoding='utf-8'):
    for row in list(chunk.values):
        if str(row[1]) in userids:
            if not country_restricted or str(genderdata[str(row[1])]["country"]) in country_restrictions:
                try:
                    timestamp = datetime.datetime.strptime(str(row[3]), datetimeFormat).date()
                    cnt += 1
                    if cnt % 1000000 == 0: logging.info(str(cnt/1000000) + " million comments computed")
                    if str(timestamp) in data:
                        data[str(timestamp)] += 1
                    else:
                        data[str(timestamp)] = 1
                except:
                    logging.warning("Could not read following line:")
                    logging.warning(str(row))
logging.info("Done (2/3)")


logging.info("Saving ...")
with open(path_results, "w") as fp:
    json.dump(data, fp)
logging.info("Done (3/3)")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))