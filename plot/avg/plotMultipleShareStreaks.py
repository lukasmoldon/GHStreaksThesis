# ---------- IMPORT ------------
import logging
import json
import datetime
import matplotlib
import matplotlib.pyplot as plt
# ------------------------------


# ---------- INPUT -------------
path_source = "C:/Users/Lukas/Desktop/streakShareValues.json"
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
with open(path_source, "r") as fp:
    plotdata = json.load(fp)


for t in plotdata:
    values = []
    for entry in plotdata[t]:
        values.append(plotdata[t][entry])
        list_of_datetimes.append(datetime.datetime.strptime(entry, datetimeFormat).date())
    dates = matplotlib.dates.date2num(list_of_datetimes)
    matplotlib.pyplot.plot_date(dates, values, '-', label="t=" + str(t))

plt.xlabel("Time")
plt.ylabel("Share of users having a streak > t")

plt.axvline(x=datetime.datetime.strptime("2016-05-19", datetimeFormat).date(), color='#D3685D', label="Design change")
plt.axvline(x=datetime.datetime.strptime("2016-12-25", datetimeFormat).date(), color='#4C4C4C', label="Christmas")
plt.axvline(x=datetime.datetime.strptime("2017-12-25", datetimeFormat).date(), color='#4C4C4C')
plt.axvline(x=datetime.datetime.strptime("2015-12-25", datetimeFormat).date(), color='#4C4C4C')
plt.legend()
plt.show()
