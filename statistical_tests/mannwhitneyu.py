# ---------- IMPORT ------------
import logging
import datetime
import json
import scipy
from scipy import stats
# ------------------------------


# ---------- INPUT -------------
path_source_x = ""
path_source_y = ""
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
# see https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html

continuity = True
alternative = "greater" # None (deprecated), "less", "two-sided", or "greater"
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
# ------------------------------



log_starttime = datetime.datetime.now()

logging.info("Accessing dataset x ...")
with open(path_source_x, "r") as fp:
    x = json.load(fp)

logging.info("Accessing dataset y ...")
with open(path_source_y, "r") as fp:
    y = json.load(fp)

logging.info("Done. (1/2)")

results = scipy.stats.mannwhitneyu(x, y, use_continuity=continuity, alternative=alternative)

logging.info("Results:" + str(results))


logging.info("Done. (2/2)")
log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))