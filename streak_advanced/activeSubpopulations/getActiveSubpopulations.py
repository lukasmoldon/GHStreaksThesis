# ---------- IMPORT ------------
import logging
import datetime
import json
# ------------------------------


# ---------- INPUT -------------
path_source = "/home/lmoldon/data/contributions_per_user_per_day.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results_2015 = "/home/lmoldon/data/activeSubpopulation2015.json"
path_results_2016 = "/home/lmoldon/data/activeSubpopulation2016.json"
# ------------------------------


# ---------- CONFIG ------------
datetimeFormat = "%Y-%m-%d"
# Min activity to be counted ...
minActivity = 50
# ... contributions(0) or days(1)...
mode = 0
# ... in this observed interval
observed_start_2015 = datetime.datetime.strptime("2015-01-01", datetimeFormat).date() 
observed_end_2015 = datetime.datetime.strptime("2015-05-19", datetimeFormat).date()
observed_start_2016 = datetime.datetime.strptime("2016-01-01", datetimeFormat).date() 
observed_end_2016 = datetime.datetime.strptime("2016-05-19", datetimeFormat).date()
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
active2015 = {}
active2016 = {}
# ------------------------------



log_starttime = datetime.datetime.now()



logging.info("Loading data ...")
with open(path_source, "r") as fp:
    contributionamount = json.load(fp)
logging.info("Done. (1/3)")


logging.info("Starting ...")
for userid in contributionamount:
    contr_2015 = 0
    contr_2016 = 0
    for timestamp in contributionamount[userid]:
        day = datetime.datetime.strptime(timestamp, datetimeFormat).date()
        if day >= observed_start_2015 and day <= observed_end_2015:
            if mode == 0:
                contr_2015 += contributionamount[userid][timestamp]
            elif mode == 1:
                contr_2015 += 1
        if day >= observed_start_2016 and day <= observed_end_2016:
            if mode == 0:
                contr_2016 += contributionamount[userid][timestamp]
            elif mode == 1:
                contr_2016 += 1
    if contr_2015 >= minActivity:
        active2015[userid] = contr_2015
    if contr_2016 >= minActivity:
        active2016[userid] = contr_2016

logging.info("Done. (2/3)")


logging.info("Saving results ...")
with open(path_results_2015, "w") as fp:
    json.dump(active2015, fp)
with open(path_results_2016, "w") as fp:
    json.dump(active2016, fp)
logging.info("Done. (3/3)")



log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))