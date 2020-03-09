# ---------- IMPORT ------------
import logging
import datetime
from datetime import timedelta, date
import json
# ------------------------------


# ---------- INPUT -------------
path_source_language = "/home/lmoldon/data/project_languages_reduced.json"
path_source_maximum = "/home/lmoldon/data/maximumStreak.json"
path_source_commits = "/home/lmoldon/data/commits_reduced.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results_stats = "/home/lmoldon/results/project_languages_distribution_streaker.json"
# ------------------------------


# ---------- CONFIG ------------
threshold = 30 # streak length
minimumContributions = 50 # minimum amount of contributions in main languages to be counted
observed_start = date(2013, 5, 19)
observed_end = date(2016, 5, 19)
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
cnt_projects = 0
cnt_languages = {} # key = langauge name, value = count
datetimeFormat = "%Y-%m-%d %H:%M:%S"
changedate = date(2016, 5, 19)
# ------------------------------



log_starttime = datetime.datetime.now()



logging.info("Loading data ...")
with open(path_source_language, "r") as fp:
    data_language = json.load(fp)
with open(path_source_maximum, "r") as fp:
    data_maximum = json.load(fp)
with open(path_source_commits, "r") as fp:
    commits = json.load(fp)
logging.info("Done. (1/3)")



logging.info("Accessing language data ...")

user_languages = {}
for userid in data_maximum:
    if data_maximum[userid] >= threshold:
        user_languages[userid] = {}


cnt_commits_total = 0

for commitid in commits:
    
    cnt_commits_total += 1
    if cnt_commits_total % 10000000 == 0:
        logging.info(str(cnt_commits_total/1000000) + " million commits computed")

    userid = str(commits[commitid]["committer_id"])
    if userid in data_maximum:
        if data_maximum[userid] >= threshold:
            try:
                performed = datetime.datetime.strptime(commits[commitid]["created_at"], datetimeFormat).date()
                if performed >= observed_start and performed <= observed_end:
                    if commits[commitid]["project_id"] in data_language:
                        if data_language[commits[commitid]["project_id"]] in user_languages[userid]:
                            user_languages[userid][data_language[commits[commitid]["project_id"]]] += 1
                        else:
                            user_languages[userid][data_language[commits[commitid]["project_id"]]] = 1
            except:
                pass
cnt_users_total = 0
for userid in data_maximum:

    cnt_users_total += 1
    if cnt_users_total % 10000 == 0:
        logging.info(str(cnt_users_total/1000) + "k users computed")

    if data_maximum[userid] >= threshold:
        maximum = 0
        maximum_lang = ""
        for lang in user_languages[userid]:
            if user_languages[userid][lang] > maximum:
                maximum = user_languages[userid][lang]
                maximum_lang = lang
        
        if maximum > minimumContributions:
            if maximum_lang in cnt_languages:
                cnt_languages[maximum_lang] += 1
            else:
                cnt_languages[maximum_lang] = 1


logging.info("Done. (2/3)")



logging.info("Storing data ...")

stats_final = dict({c: v for c, v in sorted(cnt_languages.items(), key=lambda item: item[1])})

with open(path_results_stats, "w") as fp:
    json.dump(stats_final, fp)

logging.info("Total surviving projects: " + str(cnt_projects))
logging.info("Done. (3/3)")



log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))