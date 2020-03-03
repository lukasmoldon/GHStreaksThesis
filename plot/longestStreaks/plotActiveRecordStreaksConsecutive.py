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

with open("C:/Users/Lukas/Desktop/communitysize_per_day.json", "r") as fp:
    size = json.load(fp)



with open("C:/Users/Lukas/Desktop/activeStreakRecords2015MIN15.json", "r") as fp:
    plotdata = json.load(fp)

for entry in plotdata:
    values.append(plotdata[entry]/size[str(entry)])
    list_of_datetimes.append(datetime.datetime.strptime(entry, datetimeFormat).date())



with open("C:/Users/Lukas/Desktop/activeStreakRecords2016MIN15.json", "r") as fp:
    plotdata = json.load(fp)

i = 1
for entry in plotdata:
    if i != 60: # Feb 29
        values.append(plotdata[entry]/size[str(entry)])
        list_of_datetimes.append(datetime.datetime.strptime(entry, datetimeFormat).date())
        i += 1
    else:
        i += 1



with open("C:/Users/Lukas/Desktop/activeStreakRecords2017MIN15.json", "r") as fp:
    plotdata = json.load(fp)

for entry in plotdata:
    values.append(plotdata[entry]/size[str(entry)])
    list_of_datetimes.append(datetime.datetime.strptime(entry, datetimeFormat).date())


dates = matplotlib.dates.date2num(list_of_datetimes)
matplotlib.pyplot.plot_date(dates, values, '-', label="2017")



plt.xlabel("Time", fontsize=12)
plt.ylabel("Probability of having a new personal record streak", fontsize=12)
plt.axvline(x=datetime.datetime.strptime("2016-05-19", datetimeFormat).date(), color='r', label="Streaks removed")
plt.axvline(x=datetime.datetime.strptime("2016-07-04", datetimeFormat).date(), color='g', label="Independence Day")
plt.axvline(x=datetime.datetime.strptime("2016-12-06", datetimeFormat).date(), color='k', label="GitHub Major Service Outage")
plt.legend()
plt.show()



