# ---------- IMPORT ------------
import logging
import json
import datetime
# ------------------------------


# ---------- INPUT -------------
path_source = "C:/Users/Lukas/Desktop/streakSurvivalRatesMIN15.json"
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
datetimeFormat = "%Y-%m-%d"
observed_start = datetime.datetime.strptime("2016-04-28", datetimeFormat).date()
observed_exculde = datetime.datetime.strptime("2016-05-19", datetimeFormat).date()
observed_end = datetime.datetime.strptime("2016-06-09", datetimeFormat).date()
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
data_before = 0
data_after = 0
# ------------------------------



logging.info("Accessing plot data ...")
with open(path_source, "r") as fp:
    plotdata = json.load(fp)

for entry in plotdata:
    timestamp = datetime.datetime.strptime(entry, datetimeFormat).date()
    if timestamp >= observed_start and timestamp <= observed_end:
        if timestamp > observed_exculde:
            data_after += plotdata[entry]["r"]
        elif timestamp < observed_exculde:
            data_before += plotdata[entry]["r"]


logging.info("avg before: " + str(data_before/21))
logging.info("avg after: " + str(data_after/21))
logging.info("Done.")