# ---------- IMPORT ------------
import logging
import matplotlib
import matplotlib.pyplot as plt
import datetime
import json
import ijson
from datetime import timedelta, date
# ------------------------------


# ---------- INPUT -------------
path_source_userdata = "/home/lmoldon/data/users_reduced.json"

source_IDs = []

source_names = []
# ------------------------------


# ---------- OUTPUT ------------
# ------------------------------


# ---------- CONFIG ------------
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
plotdata = {}  # key = day in observedtime, value = value of selected mode
# ------------------------------



log_starttime = datetime.datetime.now()


def getUserIdFromLogin(login):
    for userID in userdata:
        if userdata[userID]["name"] == login:
            return userID
    return -1


logging.info("Loading data ...")
with open(path_source_userdata, "r") as fp:
    userdata = json.load(fp)
logging.info("Done.")


logging.info("Starting ...")

res = {}

if source_IDs != []:
    for entry in source_IDs:
        try:
            res[entry] = userdata[entry]["name"]
        except:
            pass

if source_names != []:
    for entry in source_names:
        temp = getUserIdFromLogin(entry)
        if temp != -1:
            res[temp] = entry

logging.info("Done:")
print(res)

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))
