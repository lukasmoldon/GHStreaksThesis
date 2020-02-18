# ---------- IMPORT ------------
import logging
import datetime
import json
import datetime
from datetime import timedelta, date
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# ------------------------------


# ---------- INPUT -------------
path_source_commit = "/home/lmoldon/data/commit_comments_repaired.csv"
path_source_pullrequest = "/home/lmoldon/data/pull_request_comments_repaired.csv"

path_source_userids = "/home/lmoldon/data/users_reduced_IDs.json"
path_source_gender = "/home/lmoldon/data/users_gender.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/results/commentSentiment.json"
# ------------------------------


# ---------- CONFIG ------------
minCommentAmount = 15 # min amount of comments of a specific user
chunksize = 1000000
country_restricted = False # True == only count users from country_restrictions
country_restrictions = ["United Kingdom"]
usertype_restricted = False # True == only count users from usertype_restriction
usertype_restriction = "/home/lmoldon/results/nonStreakingUsersMAX5.json"
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d %H:%M:%S"
changedate = date(2016, 5, 19)
data = {}
globalindex = 0
analyzer = SentimentIntensityAnalyzer()
commentCounter = {}
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

logging.info("Done (1/5)")


logging.info("Computing user set ...")

for userid in userids:
    commentCounter[userid] = 0

cnt = 0
for chunk in pd.read_csv(path_source_commit, chunksize=chunksize, header=None, delimiter=",", encoding='utf-8'):
    for row in list(chunk.values):
        if str(row[2]) in userids:
            if not country_restricted or str(genderdata[str(row[2])]["country"]) in country_restrictions:
                commentCounter[str(row[2])] += 1
                cnt += 1
                if cnt % 1000000 == 0: logging.info(str(cnt/1000000) + " million commit comments computed")

cnt = 0
for chunk in pd.read_csv(path_source_pullrequest, chunksize=chunksize, header=None, delimiter=",", encoding='utf-8'):
    for row in list(chunk.values):
        if str(row[1]) in userids:
            if not country_restricted or str(genderdata[str(row[1])]["country"]) in country_restrictions:
                commentCounter[str(row[1])] += 1
                cnt += 1
                if cnt % 1000000 == 0: logging.info(str(cnt/1000000) + " million pull request comments computed")

for userid in commentCounter:
    if commentCounter[userid] < minCommentAmount:
        del userids[userid]

logging.info("Done (2/5)")


logging.info("Processing commit data ...")
cnt = 0
for chunk in pd.read_csv(path_source_commit, chunksize=chunksize, header=None, delimiter=",", encoding='utf-8'):
    for row in list(chunk.values):
        if str(row[2]) in userids:
            if not country_restricted or str(genderdata[str(row[2])]["country"]) in country_restrictions:
                try:
                    timestamp = datetime.datetime.strptime(str(row[7]), datetimeFormat).date()
                    cnt += 1
                    if cnt % 100000 == 0: logging.info(str(cnt/1000) + "k commit comments computed")
                    cur_sentiment = analyzer.polarity_scores(str(row[3]))["compound"]
                    data[str(globalindex)] = {"user": str(row[2]), "afterChange": int(timestamp >= changedate), "sentiment": float(cur_sentiment)}
                    globalindex += 1
                except:
                    logging.warning("Could not read following line:")
                    logging.warning(str(row))

logging.info("Done (3/5)")


logging.info("Processing pull request data ...")
cnt = 0
for chunk in pd.read_csv(path_source_pullrequest, chunksize=chunksize, header=None, delimiter=",", encoding='utf-8'):
    for row in list(chunk.values):
        if str(row[1]) in userids:
            if not country_restricted or str(genderdata[str(row[1])]["country"]) in country_restrictions:
                try:
                    timestamp = datetime.datetime.strptime(str(row[6]), datetimeFormat).date()
                    cnt += 1
                    if cnt % 100000 == 0: logging.info(str(cnt/1000) + "k pull request comments computed")
                    cur_sentiment = analyzer.polarity_scores(str(row[4]))["compound"]
                    data[str(globalindex)] = {"user": str(row[1]), "afterChange": int(timestamp >= changedate), "sentiment": float(cur_sentiment)}
                    globalindex += 1
                except:
                    logging.warning("Could not read following line:")
                    logging.warning(str(row))

logging.info("Done (4/5)")


logging.info("Saving ...")
with open(path_results, "w") as fp:
    json.dump(data, fp)
logging.info("Done (5/5)")

logging.info("Total number of observed users: " + str(len(userids)))
logging.info("Total number of observations: " + str(len(data)))

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))