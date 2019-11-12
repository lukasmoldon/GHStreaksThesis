# ---------- IMPORT ------------
import logging
import datetime
import json
# ------------------------------


# ---------- INPUT -------------
path_source = "/home/lmoldon/data/users_gender.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/results/countryDistribution.json"
# ------------------------------


# ---------- CONFIG ------------

# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
userdata = {}
countries = {}
# ------------------------------



log_starttime = datetime.datetime.now()


logging.info("Loading data:")

logging.info("Loading userdata ...")
with open(path_source, "r") as fp:
    userdata = json.load(fp)

logging.info("Done.")


for userid in userdata:
    cur_country = userdata[userid]["country"]
    if cur_country in countries:
        countries[cur_country] += 1
    else:
        countries[cur_country] = 1


logging.info("Saving data ...")

with open(path_results, "w") as fp:
    json.dump(countries, fp)

logging.info("Done.")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))