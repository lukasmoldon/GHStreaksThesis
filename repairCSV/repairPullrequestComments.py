# ---------- IMPORT ------------
import logging
import datetime
import json
import csv
import re
import pandas as pd
# ------------------------------


# ---------- INPUT -------------
path_source = "/home/johannes/data/github/mysql-2019-06-01/pull_request_comments.csv"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/data/pull_request_comments_repaired.csv"
# ------------------------------


# ---------- CONFIG ------------

# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
# ------------------------------


logging.info("Starting ...")
with open(path_source, "r", encoding='utf-8') as infile:
    reader = csv.reader(infile)
    globalindex = 0
    data = {}
    withinBroken = False # flag == True, if we have not found the end of a real row in current row
    currow = ""
    for row in reader: # be aware that multiple rows can correspond one single real row we want to see
        if row != []:
            if not withinBroken: # new real row starts here
                if len(row) == 7 and len(re.findall("^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$", str(row[-1]))) == 1: # this row is complete
                    row[4] = row[4].replace("\n", " ").replace("\\", "").replace(",", "").replace("\"", "").replace("\'", "").replace("`", "")
                    data[globalindex] = row
                    globalindex += 1
                    if (globalindex % 1000000 == 0):
                        logging.info(str(globalindex/1000000) + " million comments computed")
                else: # end of this new row is missing
                    i = 4
                    tmp = ""
                    while i < len(row):
                        tmp += str(row[i]).replace("\n", " ").replace("\\", "").replace(",", "").replace("\"", "").replace("\'", "").replace("`", "")
                        i += 1
                    currow = [row[0]] + [row[1]] + [row[2]] + [row[3]] + [tmp]
                    withinBroken = True
            else: # we have an open real row to be closed (find end)
                if len(re.findall("^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$", str(row[-1]))) == 1: # we found the end
                    i = 0
                    tmp = ""
                    while i < (len(row) - 2):
                        tmp += str(row[i]).replace("\n", " ").replace("\\", "").replace(",", "").replace("\"", "").replace("\'", "").replace("`", "")
                        i += 1
                    currow = [currow[0]] + [currow[1]] + [currow[2]] + [currow[3]] + [currow[4] + tmp] + [row[-2]] + [row[-1]]
                    withinBroken = False
                    currow[4] = currow[4].replace("\n", " ").replace("\\", "").replace(",", "").replace("\"", "").replace("\'", "").replace("`", "")
                    data[globalindex] = currow
                    globalindex += 1
                    if (globalindex % 1000000 == 0):
                        logging.info(str(globalindex/1000000) + " million comments computed")
                else: # no end was found - we are in the middle part of a row
                    i = 0
                    tmp = ""
                    while i < len(row):
                        tmp += str(row[i]).replace("\n", " ").replace("\\", "").replace(",", "").replace("\"", "").replace("\'", "").replace("`", "")
                        i += 1
                    currow[4] += tmp   

logging.info("Saving resulting data...")
data = pd.DataFrame.from_dict(data, "index")
data.to_csv(path_results, encoding='utf-8', index=False, header=None)
logging.info("Done!")