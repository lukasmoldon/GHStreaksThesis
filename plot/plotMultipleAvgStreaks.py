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
with open("C:/Users/Lukas/Desktop/avgStreakLength/3_years/streakValues50.json", "r") as fp:
    plotdata = json.load(fp)

for entry in plotdata:
    values.append(plotdata[entry])
    list_of_datetimes.append(datetime.datetime.strptime(entry, datetimeFormat).date())
    
dates = matplotlib.dates.date2num(list_of_datetimes)
matplotlib.pyplot.plot_date(dates, values, '-', label="x=50")
plt.xlabel("Time")
plt.ylabel("Avg. streak length")


values = []
with open("C:/Users/Lukas/Desktop/avgStreakLength/3_years/streakValues150.json", "r") as fp:
    plotdata = json.load(fp)

for entry in plotdata:
    values.append(plotdata[entry])

matplotlib.pyplot.plot_date(dates, values, '-', label="x=150")


values = []
with open("C:/Users/Lukas/Desktop/avgStreakLength/3_years/streakValues350.json", "r") as fp:
    plotdata = json.load(fp)

for entry in plotdata:
    values.append(plotdata[entry])

matplotlib.pyplot.plot_date(dates, values, '-', label="x=350")

plt.axvline(x=datetime.datetime.strptime("2016-05-19", datetimeFormat).date(), color='r')
plt.legend()
plt.show()


list_of_datetimes = []
values = []




# ------------- 7 years -------------
with open("C:/Users/Lukas/Desktop/avgStreakLength/7_years/streakValues50.json", "r") as fp:
    plotdata = json.load(fp)

for entry in plotdata:
    values.append(plotdata[entry])
    list_of_datetimes.append(datetime.datetime.strptime(entry, datetimeFormat).date())
    
dates = matplotlib.dates.date2num(list_of_datetimes)
matplotlib.pyplot.plot_date(dates, values, '-', label="x=50")
plt.xlabel("Time")
plt.ylabel("Avg. streak length")


values = []
with open("C:/Users/Lukas/Desktop/avgStreakLength/7_years/streakValues150.json", "r") as fp:
    plotdata = json.load(fp)

for entry in plotdata:
    values.append(plotdata[entry])

matplotlib.pyplot.plot_date(dates, values, '-', label="x=150")


values = []
with open("C:/Users/Lukas/Desktop/avgStreakLength/7_years/streakValues350.json", "r") as fp:
    plotdata = json.load(fp)

for entry in plotdata:
    values.append(plotdata[entry])

matplotlib.pyplot.plot_date(dates, values, '-', label="x=350")

plt.axvline(x=datetime.datetime.strptime("2016-05-19", datetimeFormat).date(), color='r')
plt.legend()
plt.show()
