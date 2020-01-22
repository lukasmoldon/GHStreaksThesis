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
x = []
values = []
# ------------------------------


lower_error = []
upper_error = []
with open("C:/Users/Lukas/Desktop/survivalAroundLastRecordMIN25DIST30BEFORE_ERRORB.json", "r") as fp:
    plotdata = json.load(fp)

del plotdata["__TOTAL__"]
del plotdata["__USERS__"]

for entry in plotdata:
    values.append(plotdata[entry]["r"])
    lower_error.append(plotdata[entry]["r"] - plotdata[entry]["a"])
    upper_error.append(plotdata[entry]["b"] - plotdata[entry]["r"])
    x.append(entry)

asymmetric_error = [lower_error, upper_error]

#matplotlib.pyplot.errorbar(x, values, yerr=asymmetric_error, fmt='o', label="Before")
plt.xlabel("Streak days arround the last record")
plt.ylabel("Survival rate of new streak within 30 days after last record")


values = []
lower_error = []
upper_error = []
with open("C:/Users/Lukas/Desktop/survivalAroundLastRecordMIN25DIST30AFTER_ERRORB.json", "r") as fp:
    plotdata = json.load(fp)

del plotdata["__TOTAL__"]
del plotdata["__USERS__"]

for entry in plotdata:
    values.append(plotdata[entry]["r"])
    lower_error.append(plotdata[entry]["r"] - plotdata[entry]["a"])
    upper_error.append(plotdata[entry]["b"] - plotdata[entry]["r"])

asymmetric_error = [lower_error, upper_error]

matplotlib.pyplot.errorbar(x, values, yerr=asymmetric_error, fmt='o', label="After")


plt.axvline(x="0", color='r', label="Last maximum streak")
plt.legend()
plt.show()
