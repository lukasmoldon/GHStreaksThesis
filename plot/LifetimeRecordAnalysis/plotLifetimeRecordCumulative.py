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
minlen = 180
maxlen = 1000
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
x = []
values = []
# ------------------------------



with open("C:/Users/Lukas/Desktop/lifetimeRecordsPlotBEFORE.json", "r") as fp:
    plotdata = json.load(fp)


i = minlen
while i <= maxlen:
    x.append(i)
    if str(i) in plotdata:
        values.append(plotdata[str(i)])
    else:
        values.append(0)
    i += 1
    
    
matplotlib.pyplot.plot(x, values, '-', label="Before")
plt.xlabel("Maximum achieved streak length in users lifetime (cumulative)")
plt.ylabel("Users in %")


values = []
with open("C:/Users/Lukas/Desktop/lifetimeRecordsPlotAFTER.json", "r") as fp:
    plotdata = json.load(fp)


i = minlen
while i <= maxlen:
    if str(i) in plotdata:
        values.append(plotdata[str(i)])
    else:
        values.append(0)
    i += 1

matplotlib.pyplot.plot(x, values, '-', label="After")

plt.legend()
plt.show()
