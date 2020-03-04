# ---------- IMPORT ------------
import logging
import json
import datetime
from datetime import timedelta, date
# ------------------------------


# ---------- INPUT -------------
path_source_userdata = "/home/lmoldon/data/users_reduced.json"
path_source_genderdata = "/home/lmoldon/data/users_gender.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/data/usergroupsizeALL.json"
path_results_male = "/home/lmoldon/data/usergroupsizeMALE.json"
path_results_female = "/home/lmoldon/data/usergroupsizeFEMALE.json"
# ------------------------------


# ---------- CONFIG ------------
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d %H:%M:%S"
groupsize = {} # store size of observed usergroup "users_reduced.json" for each day (key = date, value = size of usergroup on that day)
groupsize_female = {}
groupsize_male = {}
start_date = date(2011, 1, 1)
end_date = date(2019, 4, 1)

def daterange(observedtime_start, observedtime_end):
    for n in range(int((observedtime_end - observedtime_start).days + 1)):
        yield observedtime_start + timedelta(n)
# ------------------------------



log_starttime = datetime.datetime.now()

logging.info("Accessing userdata ...")
with open(path_source_genderdata, "r") as fp:
    genderdata = json.load(fp)
with open(path_source_userdata, "r") as fp:
    userdata = json.load(fp)
logging.info("Done (1/3)")


logging.info("Starting ...")

for day in daterange(start_date, end_date):
    groupsize[str(day)] = 0
    groupsize_male[str(day)] = 0
    groupsize_female[str(day)] = 0

cnt = 0
for userid in userdata:

    cnt += 1
    if (cnt%10000)==0: logging.info(str(cnt/1000) + "k users computed")
    
    created = datetime.datetime.strptime(str(userdata[userid]["created_at"]), "%Y-%m-%d %H:%M:%S").date()
    if created >= start_date and created <= end_date:
        for day in daterange(created, end_date):
            groupsize[str(day)] += 1
    elif created < start_date:
        for day in daterange(start_date, end_date):
            groupsize[str(day)] += 1

    if userid in genderdata:

        if genderdata[userid]["gender"] == "male":
            if created >= start_date and created <= end_date:
                for day in daterange(created, end_date):
                    groupsize_male[str(day)] += 1
            elif created < start_date:
                for day in daterange(start_date, end_date):
                    groupsize_male[str(day)] += 1

        elif genderdata[userid]["gender"] == "female":
            if created >= start_date and created <= end_date:
                for day in daterange(created, end_date):
                    groupsize_female[str(day)] += 1
            elif created < start_date:
                for day in daterange(start_date, end_date):
                    groupsize_female[str(day)] += 1

        
logging.info("Done. (2/3)")


logging.info("Storing data ...")
with open(path_results, "w") as fp:
    json.dump(groupsize, fp)
with open(path_results_male, "w") as fp:
    json.dump(groupsize_male, fp)
with open(path_results_female, "w") as fp:
    json.dump(groupsize_female, fp)
logging.info("Done. (3/3)")

logging.info("Total users: " + str(groupsize[str(end_date)]))
logging.info("Total MALE users: " + str(groupsize_male[str(end_date)]))
logging.info("Total FEMALE users: " + str(groupsize_female[str(end_date)]))

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))