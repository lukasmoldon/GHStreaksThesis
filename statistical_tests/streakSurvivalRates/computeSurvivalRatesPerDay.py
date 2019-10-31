# ---------- IMPORT ------------
import logging
import datetime
from datetime import timedelta, date
import json
# ------------------------------


# ---------- INPUT -------------
path_source_streakdata = "/home/lmoldon/data/user_streaks.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/data/streakSurvivalRates.json"
# ------------------------------


# ---------- CONFIG ------------
datetimeFormat = "%Y-%m-%d"
minLength = 15 # minimum streak length for observations
observed_start = datetime.datetime.strptime("2015-05-19", datetimeFormat).date() # start of observed time, 1 year before the change
observed_end = datetime.datetime.strptime("2017-05-20", datetimeFormat).date() # end of observed time, 1 year after the change
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
survivalRates = {} # key = date: value = {"0": #abandoned, "1": #survived}
cnt_streaks_total = 0
cnt_streaks_observed = 0
# ------------------------------



def daterange(observedtime_start, observedtime_end):
        for n in range(int((observedtime_end - observedtime_start).days)):
                yield observedtime_start + timedelta(n)


log_starttime = datetime.datetime.now()


logging.info("Loading data ...")
with open(path_source_streakdata, "r") as fp:
    streakdata = json.load(fp)
logging.info("Done (1/3)")


logging.info("Starting ...")

# Initial dict for survival rates
for single_date in daterange(observed_start, observed_end):
        survivalRates[str(single_date.strftime(datetime))] = { # day X
            "0": 0, # #abandoned (contribution on day X - 1, no contribution on day X)
            "1": 0, # #survived  (contribution on day X - 1, contribution on day X)
            "r": 0  # survival rate
        }

for userid in streakdata: # for each user
    for streakid in streakdata[userid]: # for each streak of that user

        start = datetime.datetime.strptime(str(streakdata[userid][streakid]["start"]), datetimeFormat).date()
        end = datetime.datetime.strptime(str(streakdata[userid][streakid]["end"]), datetimeFormat).date()
        length = int(streakdata[userid][streakid]["len"])
            
        cnt_streaks_total += 1
        if cnt_streaks_total % 1000000 == 0:
            logging.info(str(cnt_streaks_total/1000000) + " million streaks computed.")

        if length >= minLength and end >= observed_start and end < observed_end: # streak endpoint(!) is in observed time
            cnt_streaks_observed += 1

            if start <= observed_start: # start is not in observed time
                for single_date in daterange((observed_start + timedelta(days=1)), end):
                    survivalRates[str(single_date.strftime(datetime))]["1"] += 1
            else: # start is in observed time
                for single_date in daterange((start + timedelta(days=1)), end):
                    survivalRates[str(single_date.strftime(datetime))]["1"] += 1

            endpoint = end + timedelta(days=1) # streak abandoned on that day
            survivalRates[str(endpoint.strftime(datetime))]["0"] += 1


for date in survivalRates:
    if survivalRates[date]["0"] > 0 and survivalRates[date]["1"] > 0:
        survivalRates[date]["r"] = survivalRates[date]["1"] / (survivalRates[date]["1"] + survivalRates[date]["0"])
    elif survivalRates[date]["0"] == 0: # if both are zero, the survival rate is 1
        survivalRates[date]["r"] = 1
    elif survivalRates[date]["1"] == 0: # if abandodend number is not zero, but survived number is zero, survival rate is 0
        survivalRates[date]["r"] = 0
    

logging.info("Done. (2/3)")


logging.info("Saving results ...")
with open(path_results, "w") as fp:
    json.dump(survivalRates, fp)
logging.info("Done. (3/3)")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))