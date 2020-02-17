# ---------- IMPORT ------------
import logging
import datetime
import json
import datetime
from datetime import timedelta, date
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import statsmodels.api as sm
import random
# ------------------------------


# ---------- INPUT -------------
path_source = "/home/lmoldon/results/commentSentiment.json"

path_source_userids = "/home/lmoldon/data/users_reduced_IDs.json"
path_source_gender = "/home/lmoldon/data/users_gender.json"
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
samplesize = 10000 # number of users randomly selected for the sample
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
sentiment = []
user = []
afterChange = []

sample_userids = []
# ------------------------------



log_starttime = datetime.datetime.now()


logging.info("Loading data ...")
with open(path_source_userids, "r") as fp:
    userids = json.load(fp)

with open(path_source_gender, "r") as fp:
    genderdata = json.load(fp)

with open(path_source, "r") as fp:
    data_raw = json.load(fp)
logging.info("Done (1/4)")


logging.info("Creating user sample ...")

while len(sample_userids) < samplesize:
    userid = random.choice(list(userids.keys()))
    if userid not in sample_userids:
        sample_userids.append(userid)

logging.info("Done (2/4)")


logging.info("Creating data sample ...")

cnt = 0
cnt_observations = 0
for rowindex in data_raw:
    cnt += 1
    if (cnt%100000 == 0): logging.info(str(cnt/1000) + "k observations computed")
    if data_raw[rowindex]["user"] in sample_userids:
        cnt_observations += 1
        sentiment.append(data_raw[rowindex]["sentiment"])
        user.append(data_raw[rowindex]["user"])
        afterChange.append(data_raw[rowindex]["afterChange"])

data_pd = pd.DataFrame({"sentiment": sentiment, "user": user, "afterChange": afterChange})

logging.info("Done (3/4)")


logging.info("Computing regression ...")

mod = smf.ols(formula="sentiment ~ C(user) + afterChange", data=data_pd)
res = mod.fit()

logging.info("Results:")
print(res.summary())

logging.info("Done (3/4)")

logging.info("Observation coverage: " + str(round((cnt_observations/cnt)*100, 2)) + "%")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))