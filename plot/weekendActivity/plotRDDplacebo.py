# ---------- IMPORT ------------
import logging
import json
import datetime
from datetime import timedelta
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import colorConverter as cc
import numpy as np
# ------------------------------


# ---------- INPUT -------------
path_source = "C:/Users/Lukas/Desktop/weekendRDD_B2.json"
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
ub = []
lb = []
# ------------------------------



logging.info("Accessing plot data ...")
with open(path_source, "r") as fp:
    plotdata = json.load(fp)

for entry in plotdata:
    list_of_datetimes.append(datetime.datetime.strptime(entry, datetimeFormat).date())
    values.append(plotdata[entry]["TREATED"])
    lb.append(plotdata[entry]["a"])
    ub.append(plotdata[entry]["b"])

dates = matplotlib.dates.date2num(list_of_datetimes)
logging.info("Done. (1/2)")


logging.info("Creating plot ...")

matplotlib.pyplot.plot_date(dates, values, '-', color="#17719B")
matplotlib.pyplot.plot_date(dates, lb, '-', alpha=0.2, color="#E5C35E")
plt.axhline(0, color="black", linewidth=0.6)
plt.axhline(plotdata["2016-05-16"]["TREATED"], color="#17719B", label="On real changedate: " + str(plotdata["2016-05-16"]["TREATED"])) # 16th may for monday index
matplotlib.pyplot.plot_date(dates, ub, '-', alpha=0.2, color="#32A875")
plt.fill_between(dates, ub, values, alpha=0.3, color="#32A875")
plt.fill_between(dates, lb, values, alpha=0.3, color="#E5C35E")
plt.axvline(x=datetime.datetime.strptime("2016-05-16", datetimeFormat).date(), color='#D3685D', label="Design change", linewidth=2) # 16th may for monday index
plt.axvline(x=datetime.datetime.strptime("2016-07-04", datetimeFormat).date(), color="#8C8C8C", ls=":", label="Independence Day", linewidth=2)
plt.xlabel("Weeks in 2016", fontsize=13)
plt.ylabel("Treatment coefficient", fontsize=13)
plt.legend(fontsize=12)
plt.show()


logging.info("Done. (2/2)")