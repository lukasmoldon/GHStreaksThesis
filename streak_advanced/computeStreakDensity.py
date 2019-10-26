# ---------- IMPORT ------------
import logging
import datetime
import json
import ijson
# ------------------------------


# ---------- INPUT -------------
path_source_contributionamount = "/home/lmoldon/data/contributions_per_user_per_day.json"
path_source_streakdata = "/home/lmoldon/data/user_streaks.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/results/streakDensityValues.json"
# ------------------------------


# ---------- CONFIG ------------
minlen = 10 # minimum observed streak lentgh
binsize = 0.1 # in % size of each bin
datetimeFormat = "%Y-%m-%d"
observed_start = datetime.datetime.strptime("2014-01-01", datetimeFormat).date() # start of observed time
observed_end = datetime.datetime.strptime("2016-05-19", datetimeFormat).date() # end of observed time
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
cnt_streaks_total = 0
cnt_streaks_observed = 0
bins = {}
numberbins = 1/binsize
# ------------------------------



log_starttime = datetime.datetime.now()

def splitDaysInBins(length):
    factor = binsize
    bins_maxthreshold = []
    lastthreshold = 0
    while factor <= 1:
        newthreshold = round(factor*length)
        bins_maxthreshold.append( (lastthreshold+1, newthreshold, newthreshold-lastthreshold) )
        lastthreshold = newthreshold
        factor += 0.1
    return bins_maxthreshold # format [(start, end, sizeofbin)]

def whichbin(day, start, length):
    dayrank = (start - day).days + 1
    binsetup = splitDaysInBins(length)
    index = 0
    while index < numberbins:
        if dayrank >= binsetup[index][0] and dayrank <= binsetup[index][1]:
            return index
        else:
            index +=1
    logging.critical("Could not find a bin!")



logging.info("Loading data ...")
with open(path_source_contributionamount, "r") as fp:
    contributionamount = json.load(fp)

with open(path_source_streakdata, "r") as fp:
    streakdata = json.load(fp)
logging.info("Done (1/3)")


logging.info("Starting ...")

i = 0
while i < numberbins:
    bins[str(i)] = 0
    i += 1


for userid in streakdata:

    if userid in contributionamount:

        for streakid in streakdata[userid]:
            start = datetime.datetime.strptime(str(streakdata[userid][streakid]["start"]), datetimeFormat).date()
            end = datetime.datetime.strptime(str(streakdata[userid][streakid]["end"]), datetimeFormat).date()
            length = int(streakdata[userid][streakid]["len"])
            
            cnt_streaks_total += 1
            if cnt_streaks_total % 1000000 == 0:
                logging.info(str(cnt_streaks_total/1000000) + " million streaks computed.")

            if length >= minlen and start >= observed_start and end <= observed_end:
                cnt_streaks_observed += 1
                totalstreakcontributions = 0 # during the streak
                # setup = splitDaysInBins(length) # only divide by binsize

                tempbins = []
                i = 0
                while i < numberbins:
                    tempbins.append(0)
                    i += 1
                
                for timestamp in contributionamount[userid]:
                    day = datetime.datetime.strptime(timestamp, datetimeFormat).date()
                    if day >= start and day <= end: # day is part of current streak
                        amount = int(contributionamount[userid][timestamp])
                        totalstreakcontributions += amount
                        tempbins[whichbin(start, day, length)] += amount
            
                for index in tempbins:
                    # tempbins[index] = tempbins[index] / setup[index][2] # divide by binsize ?!
                    tempbins[index] = tempbins[index] / totalstreakcontributions # divide by totalstreakcontributions
                    bins[str(index)] += tempbins[index] # add to bins

    else:
        logging.warning("UserID " + str(userid) + ": no data found in contributions_per_user_per_day.json")
        
for index in bins:
    bins[index] = bins[index] / cnt_streaks_observed

logging.info("Done. (2/3)")


logging.info("Saving results ...")
with open(path_results, "w") as fp:
    json.dump(bins, fp)
logging.info("Done. (3/3)")


logging.info("Total streaks: " + str(cnt_streaks_total))
logging.info("Observed streaks: " + str(cnt_streaks_observed))


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))
