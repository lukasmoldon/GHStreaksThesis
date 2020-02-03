# ---------- IMPORT ------------
import logging
import json
import scipy
from scipy import stats
# ------------------------------


# ---------- INPUT -------------
path_source_x = "/home/lmoldon/results/streakLengthsMondayBefore.json"
path_source_y = "/home/lmoldon/results/streakLengthsMondayAfter.json"
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
# see https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html

continuity = True
alternative = "less" # None (deprecated), "less", "two-sided", or "greater"

# for null hypothesis (H0): 
# p <= alpha: reject H0, different distribution
# p > alpha: fail to reject H0, same distribution
alpha = 0.05
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
# ------------------------------




with open(path_source_x, "r") as fp:
    x = json.load(fp)

with open(path_source_y, "r") as fp:
    y = json.load(fp)


statistics, p = scipy.stats.mannwhitneyu(x, y, alternative=alternative, use_continuity=continuity)

logging.info("U_max = " + str(len(x)*len(y)))
logging.info("U_y = " + str(statistics))
logging.info("p = " + str(p))

if p > alpha:
	logging.info("Same distribution (fail to reject H0)")
else:
    logging.info("Different distribution (reject H0)")
