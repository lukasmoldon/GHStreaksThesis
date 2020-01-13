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
start = 70
end = 130
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
x = []
values = []
# ------------------------------


i = start
while i <= end:
    x.append(i)
    i += 1


with open("C:/Users/Lukas/Desktop/streakLengthDistributionBEFORE.json", "r") as fp:
    plotdata = json.load(fp)


i = start
while i <= end:
    if str(i) in plotdata:
        values.append(plotdata[str(i)])
    else: 
        values.append(0)
    i += 1
        
matplotlib.pyplot.plot(x, values, '-', label="Before")
plt.xlabel("Streak length distibution")
plt.ylabel("Total amount")


values = []
with open("C:/Users/Lukas/Desktop/streakLengthDistributionAFTER.json", "r") as fp:
    plotdata = json.load(fp)


i = start
while i <= end:
    if str(i) in plotdata:
        values.append(plotdata[str(i)])
    else: 
        values.append(0)
    i += 1

matplotlib.pyplot.plot(x, values, '-', label="After")

plt.legend()
plt.show()
