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



with open("C:/Users/Lukas/Desktop/survivalAroundLastRecordMIN25DIST30BEFORE.json", "r") as fp:
    plotdata = json.load(fp)

del plotdata["__TOTAL__"]

for entry in plotdata:
    values.append(plotdata[entry])
    x.append(entry)
    
matplotlib.pyplot.plot(x, values, '-', label="Before")
plt.xlabel("Streak days arround the last record")
plt.ylabel("Survival rate of new streak within 30 days after last record")


values = []
with open("C:/Users/Lukas/Desktop/survivalAroundLastRecordMIN25DIST30AFTER.json", "r") as fp:
    plotdata = json.load(fp)

del plotdata["__TOTAL__"]

for entry in plotdata:
    values.append(plotdata[entry])

matplotlib.pyplot.plot_date(x, values, '-', label="After")


plt.axvline(x="0", color='r', label="Last maximum streak")
plt.legend()
plt.show()
