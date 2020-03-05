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
minlen = 110
maxlen = 220
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
    
    
matplotlib.pyplot.plot(x, values, '-', label="Male before", color="#17719B")
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

matplotlib.pyplot.plot(x, values, '-', label="Female before", color="#D3685D")



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

matplotlib.pyplot.plot(x, values, '-', label="Male after", color="#32A875")



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

matplotlib.pyplot.plot(x, values, '-', label="Female after", color="#E5C35E")

plt.legend(fontsize=11)
plt.show()
