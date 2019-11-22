# ---------- IMPORT ------------
import logging
import datetime
import json
from datetime import timedelta, date
# ------------------------------


# ---------- INPUT -------------
path_source_subpopulation = ".."
path_source_contributionamount = "/home/lmoldon/data/contributions_per_user_per_day.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = ".."
# ------------------------------


# ---------- CONFIG ------------
k = 14 # number of days of contributions each day to be counted
year = "2015"
# ------------------------------


# ---------- INITIAL -----------
datetimeFormat = "%Y-%m-%d"
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
path_source_subpopulation = "/home/lmoldon/data/activeSubpopulation" + year + ".json"
path_results= "/home/lmoldon/results/last" + str(k) + "Days" + year + ".json"
observed_start = datetime.datetime.strptime(year + "-01-01", datetimeFormat).date()
observed_end = datetime.datetime.strptime(year + "-12-31", datetimeFormat).date()
plotdata = {}
# ------------------------------



def daterange(observedtime_start, observedtime_end):
        for n in range(int((observedtime_end - observedtime_start).days + 1)):
                yield observedtime_start + timedelta(n)



log_starttime = datetime.datetime.now()


logging.info("Loading data ...")
with open(path_source_contributionamount, "r") as fp:
    contributionamount = json.load(fp)

with open(path_source_subpopulation, "r") as fp:
    userids = json.load(fp)

for single_day in daterange(observed_start, observed_end):
    plotdata[str(single_day)] = 0
logging.info("Done. (1/3)")

logging.info("Starting ...")
cnt_user = 0
for userid in userids:
    cnt_user += 1
    if cnt_user % 10000 == 0:
        logging.info(str(cnt_user) + " users computed")
    if userid in contributionamount:
        for plotday in daterange(observed_start, observed_end):
            validStreak = True
            for single_day in daterange((plotday - timedelta(days=k-1)), plotday):
                if str(single_day) not in contributionamount[userid]:
                    validStreak = False
                    break
            if validStreak:
                plotdata[str(plotday)] += 1
    else:
        logging.warning("No contributions found for userID " + str(userid))

logging.info("Done. (2/3)")

logging.info("Saving data ...")
with open(path_results, "w") as fp:
    json.dump(plotdata, fp)
logging.info("Done. (3/3)")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))