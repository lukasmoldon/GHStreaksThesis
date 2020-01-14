# ---------- IMPORT ------------
import logging
import json
import datetime
from datetime import date, timedelta
import matplotlib
import matplotlib.pyplot as plt
# ------------------------------


# ---------- INPUT -------------

# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
k = 10
bins = [
    [20,29],
    [30,39],
    [40,49],
    [50,59],
    [60,69],
    [70,79],
    [80,89],
    [90,99],
    [100,9999999]
]
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
x = []
values = []
changedate = date(2016, 5, 19)
cnt_before = 0
cnt_after = 0
# ------------------------------


for binborder in bins:
    x.append(str(binborder[0]) + "-" + str(binborder[1]))
    values.append(0)

with open("C:/Users/Lukas/Desktop/next15Days.json", "r") as fp:
    plotdata = json.load(fp)

for day in plotdata:
    if datetime.datetime.strptime(day, datetimeFormat).date() < changedate:
        cnt_before += 1
    else:
        cnt_after += 1

for day in plotdata:
    if datetime.datetime.strptime(day, datetimeFormat).date() < changedate:
        i = 0
        for binborder in bins:
            values[i] += (( plotdata[day][str(binborder[0])]["s"] / (plotdata[day][str(binborder[0])]["s"]+plotdata[day][str(binborder[0])]["a"]) ) * 1/cnt_before)
            i += 1
        
        
matplotlib.pyplot.plot(x, values, '-', label="Before")
plt.xlabel("streak length on specific monday")
plt.ylabel("avg survival rate to specific monday + " + str(k))


values = []
for binborder in bins:
    values.append(0)

for day in plotdata:
    if datetime.datetime.strptime(day, datetimeFormat).date() >= changedate:
        i = 0
        for binborder in bins:
            values[i] += (( plotdata[day][str(binborder[0])]["s"] / (plotdata[day][str(binborder[0])]["s"]+plotdata[day][str(binborder[0])]["a"]) ) * 1/cnt_after)
            i += 1

matplotlib.pyplot.plot(x, values, '-', label="After")

plt.legend()
plt.show()
