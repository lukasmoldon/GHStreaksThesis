# ---------- IMPORT ------------
import logging
import json
import datetime
import matplotlib
import matplotlib.pyplot as plt
# ------------------------------


# ---------- INPUT -------------

# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------

# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
list_of_datetimes = []
values = []
# ------------------------------




with open("C:/Users/Lukas/Desktop/activeStreakRecords2016.json", "r") as fp:
    plotdata = json.load(fp)

i = 1
for entry in plotdata:
    if i != 60: # Feb 29
        values.append(plotdata[entry])
        list_of_datetimes.append(datetime.datetime.strptime(entry, datetimeFormat).date())
        i += 1
    else:
        i += 1
    
dates = matplotlib.dates.date2num(list_of_datetimes)
matplotlib.pyplot.plot_date(dates, values, '-', label="2016")


values = []
with open("C:/Users/Lukas/Desktop/activeStreakRecords2015.json", "r") as fp:
    plotdata = json.load(fp)

for entry in plotdata:
    values.append(plotdata[entry])

matplotlib.pyplot.plot_date(dates, values, '-', label="2015")

plt.xlabel("Time")
plt.ylabel("Number of new personal record streaks")
plt.axvline(x=datetime.datetime.strptime("2016-02-15", datetimeFormat).date(), color='c', label="President's day")
plt.axvline(x=datetime.datetime.strptime("2016-05-19", datetimeFormat).date(), color='r', label="Streaks removed (2016 only)")
plt.axvline(x=datetime.datetime.strptime("2016-05-30", datetimeFormat).date(), color='y', label="Memorial Day")
plt.axvline(x=datetime.datetime.strptime("2016-07-04", datetimeFormat).date(), color='g', label="Independence Day")
plt.axvline(x=datetime.datetime.strptime("2016-09-05", datetimeFormat).date(), color='m', label="Labor Day")
plt.axvline(x=datetime.datetime.strptime("2016-11-11", datetimeFormat).date(), color='y', label="Veteran's Day")
plt.axvline(x=datetime.datetime.strptime("2016-12-06", datetimeFormat).date(), color='k', label="GitHub Major Service Outage (2016 only)")
plt.axvline(x=datetime.datetime.strptime("2016-12-25", datetimeFormat).date(), color='b', label="Christmas")
plt.legend()
plt.show()



