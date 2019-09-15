# ---------- IMPORT ------------
import logging
import datetime
import ijson
# ------------------------------


# ---------- INPUT -------------
path_source = "/home/lmoldon/data/commits_per_user.json"
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
# format = "threshold": [over, under]
data = {
    "1": [0, 0],
    "10": [0, 0],
    "25": [0, 0],
    "50": [0, 0],
    "100": [0, 0],
    "200": [0, 0],
    "300": [0, 0],
    "400": [0, 0],
    "500": [0, 0],
    "1000": [0, 0],
    "2000": [0, 0],
    "5000": [0, 0],
}
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
# ------------------------------



log_starttime = datetime.datetime.now()

logging.info("Starting ...")

cnt=0
jsonfile = ijson.parse(open(path_source, "r"))
for prefix, event, value in jsonfile:
    if event == "number":
        cnt += 1
        for key in data:
            if value >= int(key):
                data[key][0] += 1
            else:
                data[key][1] += 1
        if cnt % 1000000 == 0:
            logging.info(str(cnt/1000000) + " million users computed.")


logging.info("Users with at least one commit total: " + str(cnt))
logging.info("Data: ")
print(data)
logging.info("Done.")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))