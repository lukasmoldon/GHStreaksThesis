# ---------- IMPORT ------------
import logging
import datetime
import json
from datetime import date, timedelta
# ------------------------------


# ---------- INPUT -------------
path_source = ""
# ------------------------------


# ---------- OUTPUT ------------
path_results = ""
# ------------------------------


# ---------- CONFIG ------------
minlen = 12
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
# ------------------------------



log_starttime = datetime.datetime.now()



log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))