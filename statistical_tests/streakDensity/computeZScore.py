# ---------- IMPORT ------------
import logging
import datetime
import json
import random
import numpy as np
import math
from datetime import date, timedelta
# ------------------------------


# ---------- INPUT -------------
path_source = "/home/lmoldon/data/contributions_per_user_per_day.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/results/zscores.json"
# ------------------------------


# ---------- CONFIG ------------
runs_per_user = 100
observed_start = date(2016, 5, 20)
observed_end = date(2017, 5, 20)
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
cnt_users_total = 0
zscores = {}
datetimeFormat = "%Y-%m-%d"
# ------------------------------



log_starttime = datetime.datetime.now()

logging.info("Loading data ...")
with open(path_source, "r") as fp:
    contributiondata = json.load(fp)
logging.info("Done (1/3)")


logging.info("Starting ...")

for userID in contributiondata:

    cnt_users_total += 1
    if cnt_users_total % 10000 == 0:
        logging.info(str(cnt_users_total/1000) + "k users computed.")

    cnt_contributions = 0
    cnt_days = 0
    cnt_real_1commitdays = 0

    for day in contributiondata[userID]:
        timestamp = datetime.datetime.strptime(day, datetimeFormat).date() 
        if timestamp >= observed_start and timestamp <= observed_end:
            cnt_days += 1
            cnt_contributions += contributiondata[userID][day]
            if contributiondata[userID][day] == 1:
                cnt_real_1commitdays += 1
    
    cnt_simulated_1commitdays = []

    i = 0
    while i < runs_per_user:

        cnt_simulated_1commitdays_TEMP = 0

        daybins = {}
        k = 0
        while k < cnt_days:
            daybins[k] = 1
            k += 1
        
        rest = cnt_contributions - cnt_days # rest of contributions
        k = 0
        while k < rest:
            daybins[random.randint(0, cnt_days-1)] += 1
            k += 1
    	
        k = 0
        while k < cnt_days:
            if daybins[k] == 1:
                cnt_simulated_1commitdays_TEMP += 1
            k += 1

        cnt_simulated_1commitdays.append(cnt_simulated_1commitdays_TEMP)
        i += 1
    
    avg = np.mean(cnt_simulated_1commitdays)
    stddeviation = 0
    for value in cnt_simulated_1commitdays:
        stddeviation += ((value - avg) ** 2)
    stddeviation = math.sqrt(stddeviation / runs_per_user)

    if stddeviation != 0:
        zscores[userID] = ((cnt_real_1commitdays - avg) / stddeviation)

logging.info("Done (2/3)")


logging.info("Saving results ...")
with open(path_results, "w") as fp:
    json.dump(zscores, fp)
logging.info("Done. (3/3)")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))