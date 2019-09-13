# ---------- IMPORT ------------
import pandas as pd
import logging
import json
import ijson
# ------------------------------


# ---------- INPUT -------------
path_source_commits = "/home/lmoldon/data/commits_reduced.json" 
path_source_issues = "/home/lmoldon/data/issues_reduced.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/data/contribution_per_user.json"
# ------------------------------


# ---------- CONFIG ------------

# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
data = {} # store dates (with time) of contribution for each user (key = userid, value = {key = date, value = 0})
ids = set() # temporary store userids of observed usergroup "users_reduced_IDs.json" in a set for better performance (membership query is faster on sets)
cnt_contributions_issues = 0
cnt_contributions_commits = 0
# ------------------------------



logging.info("Accessing issuedata ...")
cnt = 0
cur_usrid = ""
cur_usrdate = ""
cur_issueid = ""
next_step = "start"
jsonfile = ijson.parse(open(path_source_issues, "r"))
for prefix, event, value in jsonfile:

    if prefix != "" and event == "start_map":
        if next_step != "start":
            logging.critical("Corrupted data: Error at start point!")
            break
        else:
            cur_issueid = str(prefix)
            next_step = "user_id"

    elif prefix == (cur_issueid + ".userid"):
        if next_step != "user_id":
            logging.critical("Corrupted data: Error at user_id!")
            break
        else:
            cur_usrid = str(value)
            next_step = "date"

    elif prefix == (cur_issueid + ".created_at"):
        if next_step != "date":
            logging.critical("Corrupted data: Error at date!")
            break
        else:
            cur_usrdate = str(value)
            if cur_usrid in data:
                data[cur_usrid][cur_usrdate] = 0
            else:
                data[cur_usrid] = {cur_usrdate: 0}
            cnt_contributions_issues += 1
            if cnt_contributions_issues % 1000000 == 0:
                logging.info(str(cnt/1000000) + " million issues computed.")
            next_step = "end"

    elif prefix != "" and event == "end_map":
        if next_step != "end" or prefix != cur_issueid:
            logging.critical("Corrupted data: Error at end point!")
            break
        else:
            cur_usrid = ""
            cur_usrdate = ""
            cur_issueid = ""
            next_step = "start"

if next_step != "start":
    logging.critical("Corrupted data: Error at end of issuedata!")

logging.info("Done. (1/3)")


logging.info("Accessing commitdata ...")
cnt = 0
cur_usrid = ""
cur_usrdate = ""
cur_commitid = ""
next_step = "start"
jsonfile = ijson.parse(open(path_source_commits, "r"))
for prefix, event, value in jsonfile:

    if prefix != "" and event == "start_map":
        if next_step != "start":
            logging.critical("Corrupted data: Error at start point!")
            break
        else:
            cur_commitid = str(prefix)
            next_step = "user_id"

    elif prefix == (cur_commitid + ".committer_id"):
        if next_step != "user_id":
            logging.critical("Corrupted data: Error at user_id!")
            break
        else:
            cur_usrid = str(value)
            next_step = "date"

    elif prefix == (cur_commitid + ".created_at"):
        if next_step != "date":
            logging.critical("Corrupted data: Error at date!")
            break
        else:
            cur_usrdate = str(value)
            if cur_usrid in data:
                data[cur_usrid][cur_usrdate] = 0
            else:
                data[cur_usrid] = {cur_usrdate: 0}
            cnt_contributions_commits += 1
            if cnt_contributions_commits % 1000000 == 0:
                logging.info(str(cnt/1000000) + " million commits computed.")
            next_step = "end"

    elif prefix != "" and event == "end_map":
        if next_step != "end" or prefix != cur_commitid:
            logging.critical("Corrupted data: Error at end point!")
            break
        else:
            cur_usrid = ""
            cur_usrdate = ""
            cur_commitid = ""
            next_step = "start"

if next_step != "start":
    logging.critical("Corrupted data: Error at end of commitdata!")

logging.info("Done. (2/3)")


logging.info("Storing data ...")
with open(path_results, "w") as fp:
    json.dump(data, fp)

logging.info("Total contributions saved: " + str(cnt_contributions_commits + cnt_contributions_issues))
logging.info("Issues saved: " + str(cnt_contributions_issues))
logging.info("Commits saved: " + str(cnt_contributions_commits))
logging.info("Done. (3/3)")