# ---------- IMPORT ------------
import logging
import datetime
import json
import ijson
# ------------------------------


# ---------- INPUT -------------

# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
targetfile = "/home/lmoldon/data/user_streaks.json"
filesizeoverlimit = False # False = filesize < 2GB | True = filezize > 2GB
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
cnt_entries = 0
# ------------------------------



log_starttime = datetime.datetime.now()

logging.info("Starting ...")


if filesizeoverlimit:
    logging.info("Computing file size for a large file, please wait ...")
    jsonfile = ijson.parse(open(targetfile, "r"))
    for prefix, event, value in jsonfile:
        if prefix == "" and event == "map_key":
            cnt_entries += 1
            if cnt_entries % 1000000 == 0:
                logging.info(str(cnt_entries/1000000) + " million entries scanned.")

    cnt_temp = 0
    for prefix, event, value in jsonfile:
            print(str(prefix) + "|" + str(event) + "|" + str(value))
            print("--------------------------------")
            cnt_temp += 1
            if cnt_temp >= 40:
                break
else:
    logging.info("Computing file size ...")
    with open(targetfile, "r") as fp:
        jsonfile = json.load(fp)
    cnt_entries = len(jsonfile)
    logging.info(str(jsonfile)[:5000] + "  ...  }")


logging.info("Total entries in JSON file: " + str(cnt_entries))

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))