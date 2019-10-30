# ---------- IMPORT ------------
import logging
import datetime
import json
import scipy
from scipy.stats import chisquare
# ------------------------------


# ---------- INPUT -------------
path_source = "/home/lmoldon/results/contributionsPerBin.json"
# ------------------------------


# ---------- OUTPUT ------------
# ------------------------------


# ---------- CONFIG ------------
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
bindata = {}
bins = []
# ------------------------------



log_starttime = datetime.datetime.now()


logging.info("Loading data ...")
with open(path_source, "r") as fp:
    bindata = json.load(fp)
logging.info("Done (1/2)")


logging.info("Starting ...")

for index in bindata:
    bins.append(bindata[index])

result = chisquare(bins)

logging.info("Done. (2/2)")

logging.info("Chi-squared test statistic: " + str(result[0]))
logging.info("p-value: " + str(result[1]))


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))
