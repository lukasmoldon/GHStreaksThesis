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
path_source = "C:/Users/Lukas/Desktop/mondayStreakValues.json"
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
threshold = 7 # where to cut bar chart and start counting over this threshold?!
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
plotdata = {}  # key = monday type, value = {key = day in observedtime, value = value}
values = []
indices = []
maxlen = 1
avg = 0
overThreshold = 0
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
    indices = []
    maxlen = 1
    avg = 0
    overThreshold = 0

    for length in plotdata[monday_index]:
        if int(length) > maxlen:
            maxlen = int(length)

    length = 1
    while length <= maxlen:
        avg += (length * plotdata[monday_index][str(length)])
        if length > threshold:
            overThreshold += plotdata[monday_index][str(length)]
        length += 1
        

    length = 1
    while length <= threshold:
        indices.append(length)
        values.append(plotdata[monday_index][str(length)])
        length += 1


    matplotlib.pyplot.bar(indices, values)
    plt.xlabel("Exact streak length starting from " + str(observed_mondays[int(monday_index)]) + "     (Avg streak length: " + str(round(avg, 2)) + ")     (Streaks longer than " + str(threshold) + " : " + str(round(overThreshold*100, 2)) + "%)")
    plt.xticks(range(1, threshold + 1), labels=["Mon (1)", "Tue (2)", "Wed (3)", "Thu (4)", "Fri (5)", "Sat (6)", "Sun (7)", "Mon (8)", "Tue (9)", "Wed (10)", "Thu (11)", "Fri (12)", "Sat (13)", "Sun (14)"])
    plt.ylabel("Distribution of streaklengths of streaks starting on " + str(observed_mondays[int(monday_index)]))
    plt.annotate("Friday peak", xy=(5.1,0.115), xytext=(6,0.2), arrowprops=dict(facecolor='black', shrink=0.03))
    plt.show()
    


logging.info("Done.")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))