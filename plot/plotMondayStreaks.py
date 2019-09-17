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
path_source = "C:/Users/Lukas/Desktop/streakValues.json"
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------

# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
plotdata = {}  # key = monday type, value = {key = day in observedtime, value = value}
indices = []
values = []
observed_mondays = [date(2016, 4, 18), date(2016, 4, 25), date(2016, 5, 2), date(2016, 5, 9), date(
    2016, 5, 16), date(2016, 5, 23), date(2016, 5, 30), date(2016, 6, 6), date(2016, 6, 13), date(2016, 6, 20)]
# ------------------------------



log_starttime = datetime.datetime.now()


logging.info("Accessing plotdata ...")
with open(path_source, "r") as fp:
    plotdata = json.load(fp)


logging.info("Creating plot ...")

for monday_index in plotdata:
    values = []
    list_of_datetimes = []
    maxlen = 1

    for length in plotdata[monday_index]:
        if int(length) > maxlen:
            maxlen = int(length)

    length = 1
    while length <= maxlen:
        indices.append(length)
        values.append(plotdata[monday_index][str(length)])
        length += 1

    matplotlib.pyplot.bar(indices, values)
    plt.xlabel("Exact streak length starting from " + str(observed_mondays[int(monday_index)]))
    plt.ylabel("%" + " of active users on " + str(observed_mondays[int(monday_index)]))
    plt.show()
    


logging.info("Done.")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))