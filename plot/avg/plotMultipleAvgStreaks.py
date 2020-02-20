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



# ------------- 3 years -------------
with open("C:/Users/Lukas/Desktop/avgStreakLength/3_years/streakValuesY3X50.json", "r") as fp:
    plotdata = json.load(fp)

for entry in plotdata:
    values.append(plotdata[entry])
    list_of_datetimes.append(datetime.datetime.strptime(entry, datetimeFormat).date())
    
dates = matplotlib.dates.date2num(list_of_datetimes)
matplotlib.pyplot.plot_date(dates, values, '-', label="x=50")


values = []
with open("C:/Users/Lukas/Desktop/avgStreakLength/3_years/streakValuesY3X150.json", "r") as fp:
    plotdata = json.load(fp)

for entry in plotdata:
    values.append(plotdata[entry])

matplotlib.pyplot.plot_date(dates, values, '-', label="x=150")


values = []
with open("C:/Users/Lukas/Desktop/avgStreakLength/3_years/streakValuesY3X350.json", "r") as fp:
    plotdata = json.load(fp)

for entry in plotdata:
    values.append(plotdata[entry])

matplotlib.pyplot.plot_date(dates, values, '-', label="x=350")

plt.xlabel("Time")
plt.ylabel("Avg. streak length")
plt.axvline(x=datetime.datetime.strptime("2016-05-19", datetimeFormat).date(), color='r', label="Streaks removed")
plt.axvline(x=datetime.datetime.strptime("2015-05-19", datetimeFormat).date(), color='g', label="sss")
plt.axvline(x=datetime.datetime.strptime("2016-12-25", datetimeFormat).date(), color='b', label="Christmas")
plt.axvline(x=datetime.datetime.strptime("2017-12-25", datetimeFormat).date(), color='b')
plt.legend()
plt.show()
