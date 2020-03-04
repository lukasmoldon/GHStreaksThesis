# ---------- IMPORT ------------
import logging
import json
import datetime
import matplotlib
import matplotlib.pyplot as plt
# ------------------------------


# ---------- INPUT -------------
path_source_1 = "C:/Users/Lukas/Desktop/streakShareValuesUSA.json"
path_source_2 = "C:/Users/Lukas/Desktop/streakShareValuesUK.json"
path_source_3 = "C:/Users/Lukas/Desktop/streakShareValuesCHINA.json"
path_source_4 = "C:/Users/Lukas/Desktop/streakShareValuesGERMANY.json"
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
# ------------------------------



# ------------- 3 years -------------
with open(path_source_1, "r") as fp:
    plotdata_1 = json.load(fp)
with open(path_source_2, "r") as fp:
    plotdata_2 = json.load(fp)
with open(path_source_3, "r") as fp:
    plotdata_3 = json.load(fp)
with open(path_source_4, "r") as fp:
    plotdata_4 = json.load(fp)



values = []
list_of_datetimes = []
for entry in plotdata_1["20"]:
    values.append(plotdata_1["20"][entry])
    list_of_datetimes.append(datetime.datetime.strptime(entry, datetimeFormat).date())
dates = matplotlib.dates.date2num(list_of_datetimes)
matplotlib.pyplot.plot_date(dates, values, '-', label="USA", color="#17719B")

values = []
list_of_datetimes = []
for entry in plotdata_2["20"]:
    values.append(plotdata_2["20"][entry])
    list_of_datetimes.append(datetime.datetime.strptime(entry, datetimeFormat).date())
dates = matplotlib.dates.date2num(list_of_datetimes)
matplotlib.pyplot.plot_date(dates, values, '-', label="UK", color="#32A875")

values = []
list_of_datetimes = []
for entry in plotdata_3["20"]:
    values.append(plotdata_3["20"][entry])
    list_of_datetimes.append(datetime.datetime.strptime(entry, datetimeFormat).date())
dates = matplotlib.dates.date2num(list_of_datetimes)
matplotlib.pyplot.plot_date(dates, values, '-', label="China", color="#D3685D")

values = []
list_of_datetimes = []
for entry in plotdata_4["20"]:
    values.append(plotdata_4["20"][entry])
    list_of_datetimes.append(datetime.datetime.strptime(entry, datetimeFormat).date())
dates = matplotlib.dates.date2num(list_of_datetimes)
matplotlib.pyplot.plot_date(dates, values, '-', label="Germany", color="#E5C35E")




plt.xlabel("Time", fontsize=13)
plt.ylabel("Share of users having a streak of length > 20 days", fontsize=13)

plt.axvline(x=datetime.datetime.strptime("2016-05-19", datetimeFormat).date(), color='#D3685D', label="Design change")
plt.axvline(x=datetime.datetime.strptime("2016-12-25", datetimeFormat).date(), color='#8C8C8C', ls=":", label="Christmas")
plt.axvline(x=datetime.datetime.strptime("2017-12-25", datetimeFormat).date(), color='#8C8C8C', ls=":")
plt.axvline(x=datetime.datetime.strptime("2015-12-25", datetimeFormat).date(), color='#8C8C8C', ls=":")
plt.axvline(x=datetime.datetime.strptime("2016-07-04", datetimeFormat).date(), color="#8C8C8C", ls=":", label="Independence Day")
plt.axvline(x=datetime.datetime.strptime("2017-07-04", datetimeFormat).date(), color="#8C8C8C", ls=":")
plt.axvline(x=datetime.datetime.strptime("2015-07-04", datetimeFormat).date(), color="#8C8C8C", ls=":")

plt.axvline(x=datetime.datetime.strptime("2015-03-26", datetimeFormat).date(), color='#8C8C8C', ls="--", label="GitHub Server DDoS-Attack (2015)")
plt.axvline(x=datetime.datetime.strptime("2016-12-06", datetimeFormat).date(), color='#8C8C8C', ls="--", label="GitHub Major Service Outage (2016)")


plt.legend(fontsize=11)
plt.show()
