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
minlen = 30
maxlen = 110
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
x = []
values = []
# ------------------------------



with open("C:/Users/Lukas/Desktop/lifetimeRecordsPlotBEFORE_MALE.json", "r") as fp:
    plotdata = json.load(fp)


i = minlen
while i <= maxlen:
    x.append(i)
    if str(i) in plotdata:
        values.append(plotdata[str(i)])
    else:
        values.append(0)
    i += 1
    
    
matplotlib.pyplot.plot(x, values, '-', label="Male before", color="#17719B", linewidth=2)
plt.xlabel("Maximum achieved streak length in users lifetime (cumulative)", fontsize=13)
plt.ylabel("Users in %", fontsize=13)



values = []
with open("C:/Users/Lukas/Desktop/lifetimeRecordsPlotBEFORE_FEMALE.json", "r") as fp:
    plotdata = json.load(fp)


i = minlen
while i <= maxlen:
    if str(i) in plotdata:
        values.append(plotdata[str(i)])
    else:
        values.append(0)
    i += 1

matplotlib.pyplot.plot(x, values, '-', label="Female before", color="#D3685D", linewidth=2)



values = []
with open("C:/Users/Lukas/Desktop/lifetimeRecordsPlotAFTER_MALE.json", "r") as fp:
    plotdata = json.load(fp)


i = minlen
while i <= maxlen:
    if str(i) in plotdata:
        values.append(plotdata[str(i)])
    else:
        values.append(0)
    i += 1

matplotlib.pyplot.plot(x, values, '-', label="Male after", color="#32A875", linewidth=2)



values = []
with open("C:/Users/Lukas/Desktop/lifetimeRecordsPlotAFTER_FEMALE.json", "r") as fp:
    plotdata = json.load(fp)

i = minlen
while i <= maxlen:
    if str(i) in plotdata:
        values.append(plotdata[str(i)])
    else:
        values.append(0)
    i += 1

matplotlib.pyplot.plot(x, values, '-', label="Female after", color="#E5C35E", linewidth=2)

plt.legend(fontsize=11)
plt.show()
