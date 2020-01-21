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
minlen = 20
maxlen = 100
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
x = []
values = []
# ------------------------------



with open("/home/lmoldon/results/lifetimeRecordsPlotBEFORE.json", "r") as fp:
    plotdata = json.load(fp)


i = minlen
while i <= maxlen:
    x.append(str(i))
    if str(i) in plotdata:
        values.append(plotdata[str(i)])
    else:
        values.append(0)
    i += 1
    
    
matplotlib.pyplot.plot(x, values, '-', label="Before")
plt.xlabel("Maximum streak length in users lifetime")
plt.ylabel("Users in %")


values = []
with open("/home/lmoldon/results/lifetimeRecordsPlotAFTER.json", "r") as fp:
    plotdata = json.load(fp)


i = minlen
while i <= maxlen:
    if str(i) in plotdata:
        values.append(plotdata[str(i)])
    else:
        values.append(0)
    i += 1

matplotlib.pyplot.plot_date(x, values, '-', label="After")

plt.legend()
plt.show()
