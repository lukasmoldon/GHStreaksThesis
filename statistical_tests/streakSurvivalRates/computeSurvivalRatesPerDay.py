# ---------- IMPORT ------------
import logging
import datetime
from datetime import timedelta, date
import json
import numpy as np
import random
import scipy.stats
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
confidenceInterval = 95 # in %
amountSamples = 1000 # number of bootstrapped samples per day
observed_start = datetime.datetime.strptime("2015-05-19", datetimeFormat).date() # start of observed time, 1 year before the change
observed_end = datetime.datetime.strptime("2017-05-20", datetimeFormat).date() # end of observed time, 1 year after the change
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
survivalRates = {} # key = date: value = {"0": #abandoned, "1": #survived}
cnt_streaks_total = 0
cnt_streaks_observed = 0
lowerbound = (100 - confidenceInterval) / 2
upperbound = confidenceInterval + (100 - confidenceInterval) / 2
# ------------------------------



def daterange(observedtime_start, observedtime_end):
        for n in range(int((observedtime_end - observedtime_start).days + 1)):
                yield observedtime_start + timedelta(n)

def createBootstrapSample(data):
    i = 0
    bootstrapSample = []
    while i < len(data):
        bootstrapSample.append(random.choice(data))
        i += 1
    return bootstrapSample

def getBootstrapSampleAvgs(survived, abandoned, amountSamples):
    sampleAvgs = []
    base = [0] * survived + [1] * abandoned
    random.shuffle(base)
    i = 0
    while i < amountSamples:
        sampleAvgs.append(np.mean(createBootstrapSample(base)))
        i += 1
    return sampleAvgs



log_starttime = datetime.datetime.now()


logging.info("Loading data ...")
with open(path_source_streakdata, "r") as fp:
    streakdata = json.load(fp)
logging.info("Done (1/4)")


logging.info("Calculating survival rates...")

# Initial dict for survival rates
for single_date in daterange(observed_start, observed_end):
        survivalRates[str(single_date.strftime(datetimeFormat))] = { # day X
            "0": 0, # #abandoned (contribution on day X - 1, no contribution on day X)
            "1": 0, # #survived  (contribution on day X - 1, contribution on day X)
            "r": 0, # survival rate (avg)
            "a": 0, # 2.5th% of x bootstrapped avg values (lower bound of 95% confidence interval)
            "b": 0  # 97.5th% of x bootstrapped avg values (upper bound of 95% confidence interval)
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
                    survivalRates[str(single_date.strftime(datetimeFormat))]["1"] += 1
            else: # start is in observed time
                for single_date in daterange((start + timedelta(days=1)), end):
                    survivalRates[str(single_date.strftime(datetimeFormat))]["1"] += 1

            endpoint = end + timedelta(days=1) # streak abandoned on that day
            survivalRates[str(endpoint.strftime(datetimeFormat))]["0"] += 1


for date in survivalRates:
    if survivalRates[date]["0"] > 0 and survivalRates[date]["1"] > 0:
        survivalRates[date]["r"] = survivalRates[date]["1"] / (survivalRates[date]["1"] + survivalRates[date]["0"])
    elif survivalRates[date]["0"] == 0: # if both are zero, the survival rate is 1
        survivalRates[date]["r"] = 1
    elif survivalRates[date]["1"] == 0: # if abandoned number is not zero, but survived number is zero, survival rate is 0
        survivalRates[date]["r"] = 0
    
logging.info("Done. (2/4)")


logging.info("Calculating confidence intervals ...")
i = 0
for date in survivalRates:
    sampleAvgs = getBootstrapSampleAvgs(survivalRates[date]["0"], survivalRates[date]["1"], amountSamples)
    survivalRates[date]["a"] = np.percentile(sampleAvgs, lowerbound)
    survivalRates[date]["b"] = np.percentile(sampleAvgs, upperbound)
    i += 1
    if i % 100 == 0:
        logging.info(str(i) + " days computed.") 

logging.info("Done. (3/4)")


logging.info("Saving results ...")
with open(path_results, "w") as fp:
    json.dump(survivalRates, fp)
logging.info("Done. (4/4)")


logging.info("Total streaks: " + str(cnt_streaks_total))
logging.info("Observed streaks: " + str(cnt_streaks_observed))

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))