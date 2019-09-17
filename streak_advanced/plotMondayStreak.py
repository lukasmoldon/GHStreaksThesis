# ---------- IMPORT ------------
import logging
import matplotlib
import matplotlib.pyplot as plt
import datetime
import json
import ijson
from datetime import timedelta, date
# ------------------------------


# ---------- INPUT -------------
path_source_streakdata = "/home/lmoldon/data/user_streaks.json"
path_source_usergroupsize = "/home/lmoldon/data/usergroupsize.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results_values = "/home/lmoldon/results/streakValues.json"
# ------------------------------


# ---------- CONFIG ------------
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
plotdata = {"0": {}, "1": {}, "2": {}, "3": {}, "4": {}, "5": {}, "6": {}, "7": {
}, "8": {}, "9": {}}  # key = monday type, value = {key = streaklength, value = value}
start = date(1970, 1, 1)
end = date(1970, 1, 1)
list_of_datetimes = []
values = []
observed_mondays = [date(2016, 4, 18), date(2016, 4, 25), date(2016, 5, 2), date(2016, 5, 9), date(
    2016, 5, 16), date(2016, 5, 23), date(2016, 5, 30), date(2016, 6, 6), date(2016, 6, 13), date(2016, 6, 20)]
# ------------------------------


log_starttime = datetime.datetime.now()


logging.info("Starting ...")

streakdata = ijson.parse(open(path_source_streakdata, "r"))
for prefix, event, value in streakdata:
    if ".start" in prefix:
        start = datetime.datetime.strptime(str(value), datetimeFormat).date()
        cnt_streaks += 1
        if cnt_streaks % 1000000 == 0:
            logging.info(str(cnt_streaks/1000000) +
                         " million streaks computed.")
    elif ".end" in prefix:
        end = datetime.datetime.strptime(str(value), datetimeFormat).date()
    elif ".len" in prefix:
        if start in observed_mondays:
            monday_index = str(observed_mondays.index(start))
            if str(value) in plotdata[monday_index]:
                plotdata[monday_index][str(value)] += 1
            else:
                plotdata[monday_index][str(value)] = 1

logging.info("Done. (1/2)")


logging.info("Creating plot data ...")


for monday_index in plotdata:  # get %
    maxlen = 1
    cnt_streaks = 0

    for length in plotdata[monday_index]: 
        cnt_streaks += plotdata[monday_index][length]
        if int(length) > maxlen:
            maxlen = int(length)
    
    i = 1
    while i < maxlen:
        if not (str(i) in plotdata[monday_index]):
            plotdata[monday_index][str(i)] = 0
        i += 1

    for length in plotdata[monday_index]:
        plotdata[monday_index][length] = (plotdata[monday_index][length] / cnt_streaks)



logging.info("Saving plot data ...")

with open(path_results_values, "w") as fp:
    json.dump(plotdata, fp)


logging.info("Done. (2/2)")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))
