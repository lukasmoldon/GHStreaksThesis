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
observed_mondays = [
    date(2016, 1, 4), 
    date(2016, 1, 11),
    date(2016, 1, 18), 
    date(2016, 1, 25), 
    date(2016, 2, 1), 
    date(2016, 2, 8), 
    date(2016, 2, 15), 
    date(2016, 2, 22), 
    date(2016, 2, 29), 
    date(2016, 3, 7)
    ]
# ------------------------------



log_starttime = datetime.datetime.now()


logging.info("Accessing plotdata ...")
with open(path_source, "r") as fp:
    plotdata = json.load(fp)


averaged = {}
for monday in observed_mondays:
    for length in plotdata[str(monday)]:
        averaged[length] = 0

for monday in observed_mondays:
    for length in plotdata[str(monday)]:
        averaged[length] += plotdata[str(monday)][length]

for length in averaged:
    averaged[length] /= len(observed_mondays)



logging.info("Creating plot ...")


values = []
indices = []
maxlen = 1
avg = 0
overThreshold = 0

for length in averaged:
    if int(length) > maxlen:
        maxlen = int(length)


length = 1
while length <= maxlen:
    avg += (length * averaged[str(length)])
    if length > threshold:
        overThreshold += averaged[str(length)]
    length += 1
        

length = 1
while length <= threshold:
    indices.append(length)
    values.append(averaged[str(length)])
    length += 1


matplotlib.pyplot.bar(indices, values, color="#17719B")
plt.xlabel("Streak length in days \n" + "     (Avg streak length: " + str(round(avg, 2)) + ")     (Streaks longer than " + str(threshold) + " : " + str(round(overThreshold*100, 2)) + "%)", fontsize=12)
plt.xticks(range(1, threshold + 1), labels=["Mon (1)", "Tue (2)", "Wed (3)", "Thu (4)", "Fri (5)", "Sat (6)", "Sun (7)", "Mon (8)", "Tue (9)", "Wed (10)", "Thu (11)", "Fri (12)", "Sat (13)", "Sun (14)"])
plt.ylabel("Share of streaklengths", fontsize=12)
plt.annotate("Friday peak", xy=(5.1,0.115), xytext=(6,0.2), arrowprops=dict(facecolor='black', shrink=0.03), fontsize=12)
plt.show()
    


logging.info("Done.")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))