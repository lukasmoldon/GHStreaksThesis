# ---------- IMPORT ------------
import logging
import datetime
import json
# ------------------------------


# ---------- INPUT -------------
path_source_data = "/home/lmoldon/data/users_gender.json"
path_source_merge = "/home/lmoldon/data/merge.json"
path_source_mergeContinents = "/home/lmoldon/data/mergeContinents.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results_country = "/home/lmoldon/results/countryDistribution.json"
path_results_continent = "/home/lmoldon/results/continentDistribution.json"
# ------------------------------


# ---------- CONFIG ------------

# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
userdata = {}
merge = {}
mergeContinents = {}

countries = {}
continents = {}
# ------------------------------



log_starttime = datetime.datetime.now()



logging.info("Loading data ...")
with open(path_source_data, "r") as fp:
    userdata = json.load(fp)

with open(path_source_merge, "r") as fp:
    merge = json.load(fp)

with open(path_source_mergeContinents, "r") as fp:
    mergeContinents = json.load(fp)

logging.info("Done. (1/3)")


logging.info("Starting ...")

for userid in userdata:
    cur_country = userdata[userid]["country"]
    if cur_country in merge:
        cur_country = merge[cur_country]

    if cur_country in countries:
        countries[cur_country] += 1
    else:
        countries[cur_country] = 1
    
    if cur_country in mergeContinents:
        if mergeContinents[cur_country] in continents:
            continents[mergeContinents[cur_country]] += 1
        else:
            continents[mergeContinents[cur_country]] = 1
    else:
        if "Unknown" in continents:
            continents["Unknown"] += 1
        else:
            continents["Unknown"] = 1


continents_final = dict({c: v for c, v in sorted(continents.items(), key=lambda item: item[1])})
countries_final = dict({c: v for c, v in sorted(countries.items(), key=lambda item: item[1])})

logging.info("Done. (2/3)")


logging.info("Saving data ...")

with open(path_results_country, "w") as fp:
    json.dump(countries_final, fp)

with open(path_results_continent, "w") as fp:
    json.dump(continents_final, fp)

logging.info("Done. (3/3)")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))