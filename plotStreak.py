# ---------- IMPORT ------------
import logging
import matplotlib.pyplot as plt
import datetime
import json
import ijson
from datetime import timedelta, date
# ------------------------------


# ---------- INPUT -------------
path_source_streakdata = "/home/lmoldon/results/user_streaks.json"
path_source_groupdata = "/home/lmoldon/results/user_groups.json"
path_source_usergroupsize = "/home/lmoldon/data/usergroupsize.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results_values = "/home/lmoldon/results/streakValues.json"
path_results_plot = "/home/lmoldon/results/streakPlot.png"
# ------------------------------


# ---------- CONFIG ------------
threshold = 50 # minimum streak length to get plotted
mode = 0 # 0 = plot avg streak length, 1 = plot avg number of streaks
observedtime_start = date(2015, 1, 1)
observedtime_end = date(2017, 12, 31)
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
plotdata = {} # key = day in observedtime, value = value of selected mode
start = date(1970, 1, 1)
end = date(1970, 1, 1)
# ------------------------------



def daterange(observedtime_start, observedtime_end):
        for n in range(int((observedtime_end - observedtime_start).days)):
                yield observedtime_start + timedelta(n)


for single_date in daterange(observedtime_start, observedtime_end):
        plotdata[str(single_date.strftime("%Y-%m-%d"))] = 0


logging.info("Accessing usergroupsize data ...")
with open(path_source_usergroupsize, "r") as fp:
    usergroupsize = json.load(fp)

logging.info("Done. (1/3)")


logging.info("Accessing usergroup data ...")
with open(path_source_groupdata, "r") as fp:
    groupdata = json.load(fp)

logging.info("Done. (2/3)")


logging.info("Starting ...")
streakdata = ijson.parse(open(path_source_streakdata, "r"))
cnt = 0
for prefix, event, value in streakdata:
    if ".start" in prefix:
        start = datetime.datetime.strptime(str(value), datetimeFormat).date()
        cnt += 1
        if cnt % 1000000 == 0: 
            logging.info(str(cnt/1000000) + " million streaks computed.")
    elif ".end" in prefix:
        end = datetime.datetime.strptime(str(value), datetimeFormat).date()
    elif ".len" in prefix:
        if int(value) >= threshold:
                if start <= observedtime_end and end >= observedtime_start: # streak happend (partially) in observed time
                        if start >= observedtime_start: # start in observed time
                                if end <= observedtime_end: # start and end in observed time
                                        for single_date in daterange(start, end):
                                            if mode == 0:
                                                plotdata[str(single_date)] += ((single_date - start) + timedelta(days=1)).days
                                            elif mode == 1:
                                                plotdata[str(single_date)] += 1
                                else: # start in observed time, end not in observed time
                                        for single_date in daterange(start, observedtime_end):
                                                if mode == 0:
                                                    plotdata[str(single_date)] += ((single_date - start) + timedelta(days=1)).days
                                                elif mode == 1:
                                                    plotdata[str(single_date)] += 1
                        else: # start not in observed time
                                if end <= observedtime_end: # start not in observed time, but end in observed time
                                        for single_date in daterange(observedtime_start, end):
                                                if mode == 0:
                                                    plotdata[str(single_date)] += ((single_date - start) + timedelta(days=1)).days
                                                elif mode == 1:
                                                    plotdata[str(single_date)] += 1
                                else: # start and end not in observed time
                                        for single_date in daterange(observedtime_start, observedtime_end):
                                                if mode == 0:
                                                    plotdata[str(single_date)] += ((single_date - start) + timedelta(days=1)).days
                                                elif mode == 1:
                                                    plotdata[str(single_date)] += 1


# TODO: Create .png file

logging.info("Plot image saved.")
logging.info("Done. (3/3)")
logging.info("Data:")
print(plotdata)