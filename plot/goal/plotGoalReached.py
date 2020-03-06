# ---------- IMPORT ------------
import logging
import json
import datetime
import matplotlib
import matplotlib.pyplot as plt
# ------------------------------


# ---------- INPUT -------------
path_source = "C:/Users/Lukas/Desktop/goalAchiever.json"
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
c = ["#17719B", "#32A875", "#D3685D", "#E5C35E"]
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
# ------------------------------



# ------------- 3 years -------------
with open(path_source, "r") as fp:
    plotdata = json.load(fp)

i = 0
for t in plotdata:
    values = []
    list_of_datetimes = []
    for entry in plotdata[t]:
        values.append(plotdata[t][entry])
        list_of_datetimes.append(datetime.datetime.strptime(entry, datetimeFormat).date())
    dates = matplotlib.dates.date2num(list_of_datetimes)
    matplotlib.pyplot.plot_date(dates, values, '-', label="g=" + str(t), color=c[i])
    i += 1

plt.xlabel("Time", fontsize=13)
plt.ylabel("Number of users reached streak goal g", fontsize=13)

plt.axvline(x=datetime.datetime.strptime("2016-05-19", datetimeFormat).date(), color='#D3685D', label="Design change")


plt.legend(fontsize=11)
plt.show()
