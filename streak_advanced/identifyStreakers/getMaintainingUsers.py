# ---------- IMPORT ------------
import logging
import datetime
from datetime import timedelta
import json
# ------------------------------


# ---------- INPUT -------------
path_source_streakdata = "/home/lmoldon/data/user_streaks.json"
path_source_userdata = "/home/lmoldon/data/users_reduced.json"
path_source_genderdata = "/home/lmoldon/data/users_gender.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "..."
# ------------------------------


# ---------- CONFIG ------------
minlen = 32 # min streak length to be counted
offset = 5 # streak has to start before changedate + offset
minSurvival = 32 # streak has to end after changedate + minSurvival
changedate = datetime.date(2016, 5, 19)
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
maintain_ids = {}
cnt_female = 0
cnt_male = 0
cnt_unknown = 0
path_results = "/home/lmoldon/results/maintainingUsersMIN" + str(minlen) + ".json"
# ------------------------------



log_starttime = datetime.datetime.now()


logging.info("Loading data ...")
with open(path_source_streakdata, "r") as fp:
    streakdata = json.load(fp)

with open(path_source_userdata, "r") as fp:
    userids = json.load(fp)

with open(path_source_genderdata, "r") as fp:
    genderdata = json.load(fp)
logging.info("Done (1/3)")


logging.info("Starting...")
cnt_streaks_total = 0

for userid in streakdata:  # for each user
    
    for streakid in streakdata[userid]:  # for each streak of that user

        start = datetime.datetime.strptime(str(streakdata[userid][streakid]["start"]), datetimeFormat).date()
        end = datetime.datetime.strptime(str(streakdata[userid][streakid]["end"]), datetimeFormat).date()
        length = int(streakdata[userid][streakid]["len"])

        cnt_streaks_total += 1
        if cnt_streaks_total % 1000000 == 0:
            logging.info(str(cnt_streaks_total/1000000) + " million streaks computed.")

        if end >= (changedate + timedelta(days=minSurvival)) and start <= (changedate + timedelta(days=offset)) and length >= minlen:
            if userid in maintain_ids:
                maintain_ids[userid] = max(length, maintain_ids[userid])
            else:
                maintain_ids[userid] = length
                if userid in genderdata:
                    if genderdata[userid]["gender"] == "male":
                        cnt_male += 1
                    elif genderdata[userid]["gender"] == "female":
                        cnt_female += 1
                    else:
                        cnt_unknown += 1
                else:
                    logging.debug("UserID " + userid + " not in gender data.")
                    cnt_unknown += 1



logging.info("Done. (2/3)")


logging.info("Saving results ...")
with open(path_results, "w") as fp:
    json.dump(maintain_ids, fp)
logging.info("Done. (3/3)")

logging.info("Total number of maintaining users: " + str(len(maintain_ids)))
logging.info("Gender distribution:")
print("male: " + str(cnt_male))
print("female: " + str(cnt_female))
print("unknown: " + str(cnt_unknown))

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))