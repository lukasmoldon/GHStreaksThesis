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
path_results = "/home/lmoldon/results/streakOneContributionDaysShare.json"
# ------------------------------


# ---------- CONFIG ------------
minlen = 60 # minimum observed streak lentgh
binsize = 0.1 # in % size of each bin
datetimeFormat = "%Y-%m-%d"
observed_start = datetime.datetime.strptime("2015-05-19", datetimeFormat).date() # start of observed time, 1 year before the change
observed_end = datetime.datetime.strptime("2016-05-19", datetimeFormat).date() # end of observed time, day of the change
#observed_start = datetime.datetime.strptime("2016-05-20", datetimeFormat).date() # start of observed time, one day after the change
#observed_end = datetime.datetime.strptime("2017-05-20", datetimeFormat).date() # end of observed time, 1 year after the change
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
cnt_streaks_total = 0
cnt_streaks_observed = 0
bins = {}
numberbins = round(1/binsize)
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
        factor += binsize
    return bins_maxthreshold # format [(start, end, sizeofbin)]

def whichbin(day, start, length):
    dayrank = (day - start).days + 1
    binsetup = splitDaysInBins(length)
    index = 0
    while index < numberbins:
        if dayrank >= binsetup[index][0] and dayrank <= binsetup[index][1]:
            return index
        else:
            index +=1
    logging.critical("Could not find a bin!")
    logging.critical("Binsetup: " + str(binsetup))
    logging.critical("Dayrank: " + str(dayrank))



logging.info("Loading data ...")
with open(path_source_contributionamount, "r") as fp:
    contributionamount = json.load(fp)

with open(path_source_streakdata, "r") as fp:
    streakdata = json.load(fp)
logging.info("Done (1/3)")


logging.info("Starting ...")

i = 0
while i < numberbins:
    bins[i] = 0
    i += 1


for userid in streakdata: # for each user

    if userid in contributionamount:

        for streakid in streakdata[userid]: # for each streak of that user
            
            start = datetime.datetime.strptime(str(streakdata[userid][streakid]["start"]), datetimeFormat).date()
            end = datetime.datetime.strptime(str(streakdata[userid][streakid]["end"]), datetimeFormat).date()
            length = int(streakdata[userid][streakid]["len"])
            
            cnt_streaks_total += 1
            if cnt_streaks_total % 1000000 == 0:
                logging.info(str(cnt_streaks_total/1000000) + " million streaks computed.")

            if length >= minlen and start >= observed_start and end <= observed_end:
                cnt_streaks_observed += 1
                setup = splitDaysInBins(length) # only for binsize

                tempbins = {}
                tempbinsNoOCD = {}
                i = 0
                while i < numberbins:
                    tempbins[i] = 0
                    tempbinsNoOCD[i] = 0
                    i += 1
                
                for timestamp in contributionamount[userid]:
                    day = datetime.datetime.strptime(timestamp, datetimeFormat).date()
                    amount = int(contributionamount[userid][timestamp])
                    if day >= start and day <= end and amount == 1: # day is part of current streak AND there was only one contribution!
                        tempbins[whichbin(day, start, length)] += 1
                    elif day >= start and day <= end and amount > 1: # day is part of current streak AND there was more than one contribution!
                        tempbinsNoOCD[whichbin(day, start, length)] += 1
            
                for index in tempbins: # calculate avg share of 1 contribution days (bins dont always have same size)
                    tempbins[index] = tempbins[index] / setup[index][2] # divide by binsize
                    tempbinsNoOCD[index] = tempbinsNoOCD[index] / setup[index][2] # divide by binsize

                for index in tempbins: # calculate distibution over all bins in %
                    tempbins[index] = tempbins[index] / (tempbins[index] + tempbinsNoOCD[index]) # divide by number of observed days
                    bins[index] += tempbins[index] # add to bins
                    
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
