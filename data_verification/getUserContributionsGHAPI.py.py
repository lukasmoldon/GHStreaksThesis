# ---------- IMPORT ------------
import requests
import requests_html
import datetime
from datetime import timedelta
import json
import time
import logging
import sys
# ------------------------------


# ---------- INPUT -------------
path_source_userdata = "/home/lmoldon/data/users_reduced.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "..."
# ------------------------------


# ---------- CONFIG ------------
username = "XXXXXXXXXXXXXXXXXXXXX"
token = "XXXXXXXXXXXXXXXXXXXXX"
email = "XXXXXXXXXXXXXXXXXXXXX"
useragent = "Research for bachelor thesis on GitHub streaks"

chunksize = 1000000

debugmode = False # Enable debug messages in console
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
userdata = {} # from reduced_users
userid = sys.argv[1]
path_results = "/home/lmoldon/results/verification/contributions_" + userid + ".json"

if debugmode:
    logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.DEBUG)
else:
    logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)

useragent = useragent + "  Contact: " + email
session = requests_html.HTMLSession()

link_userinfo = "https://api.github.com/users/"

nextreq = datetime.datetime.now()

repo_collection = set()

queryresult = {}
# ------------------------------



def sleep_epoch(epochtime):
    start = datetime.datetime.fromtimestamp(int(epochtime) + 10)
    now = datetime.datetime.now().replace(microsecond=0)
    logging.info("Waiting for API counter reset in " + str(start - now))
    time.sleep((start - now).seconds)
    logging.info("Stopped waiting!")



log_starttime = datetime.datetime.now()



logging.info("Loading userdata ...")

with open(path_source_userdata, "r") as fp:
    userdata = json.load(fp)

cur_username = userdata[userid]["name"]
link_userrepo = "https://api.github.com/users/" + cur_username + "/repos?per_page=100&page="

logging.info("Done.")



logging.info("Connecting with api.github.com:")

cnt_triesGH = 0
done = False
while(not done):
    try:
        answer = session.get(link_userinfo + "lukasmoldon", auth=(username, token))
        time.sleep(0.72)

        status = answer.headers["Status"]
        if status != "200 OK":
            if int(answer.headers["X-RateLimit-Remaining"]) == 0:
                logging.info("API counter at 0!")
                sleep_epoch(answer.headers["X-RateLimit-Reset"])
                answer = session.get(link_userinfo + "lukasmoldon", auth=(username, token))
                time.sleep(0.72)

        if status == "200 OK":
            done = True
            logging.info("Requests remaining for GitHub API: " + str(int(answer.headers["X-RateLimit-Remaining"])))
        else:
            logging.error("Received unexpected answer while connecting with api.github.com:")
            print(answer.headers)
            print(answer.text)
            time.sleep(0.72)
            cnt_triesGH += 1
            if cnt_triesGH > 50:
                logging.fatal("Too many failed GET requests without 200 OK:")
                print(answer.headers)
                print(answer.text)
                sys.exit()
    except Exception as e:
        logging.warning("Could not send GET request to api.github.com")
        print(e)
        time.sleep(0.72)
        cnt_triesGH += 1
        if cnt_triesGH > 50:
            logging.fatal("Too many failed GET requests")
            sys.exit()

logging.info("Done.")



logging.info("Collecting ...")


answer = ["_"]
repo_page = 0
while(len(answer) > 0):
    repo_page += 1
    done = False
    skip = False
    while(not done):
        try:
            answer = session.get(link_userrepo + str(repo_page), auth=(username, token))
            time.sleep(0.72)

            status = answer.headers["Status"]
            if status == "404 Not Found" or status == "403 Forbidden":
                done = True
                skip = True
            elif status != "200 OK":
                if int(answer.headers["X-RateLimit-Remaining"]) == 0:
                    logging.info("API counter at 0!")
                    sleep_epoch(answer.headers["X-RateLimit-Reset"])
                    answer = session.get(link_userrepo + str(repo_page), auth=(username, token))
                    time.sleep(0.72)

            if not skip:
                if status == "200 OK":
                    done = True
                else:
                    logging.error("Received unexpected answer while connecting with api.github.com:")
                    print(link_userinfo + cur_username)
                    print(answer.headers)
                    print(answer.text)
                    time.sleep(0.72)
                    cnt_triesGH += 1
                    if cnt_triesGH > 50:
                        logging.fatal("Too many failed GET requests without 200 OK:")
                        print(link_userinfo + cur_username)
                        print(answer.headers)
                        print(answer.text)
                        sys.exit()
        except Exception as e:
            logging.warning("Could not send GET request to api.github.com")
            print(e)
            time.sleep(0.72)
            cnt_triesGH += 1
            if cnt_triesGH > 50:
                logging.critical("Too many failed GET requests. Waiting 60 min ...")
                time.sleep(3600)
            elif cnt_triesGH > 70:
                logging.fatal("Too many failed GET requests")
                sys.exit()

    try:
        if int(answer.headers["X-RateLimit-Remaining"]) % 1000 == 0:
            logging.info("GitHub requests remaining: " + str(answer.headers["X-RateLimit-Remaining"]))
    except:
        pass
            
    if not skip:
        try:
            for repo in answer.json():
                repo_collection.add(repo["url"])
        except Exception as e:
            logging.debug("Could not compute repo entries for: " + str(cur_username))
            print(e)
    else:
        logging.debug("Username not found: " + str(cur_username))

    try:        
        answer = answer.json()
    except:
        answer = ["_"]

for link_repo in repo_collection:
    commit_page = 0
    link_repo = link_repo + "/commits?per_page=100&page="
    answer = ["_"]

    while(len(answer) > 0):
        commit_page += 1
        while(not done):
            try:
                answer = session.get(link_repo + str(commit_page), auth=(username, token))
                time.sleep(0.72)

                status = answer.headers["Status"]
                if status == "404 Not Found" or status == "403 Forbidden":
                    done = True
                    skip = True
                elif status != "200 OK":
                    if int(answer.headers["X-RateLimit-Remaining"]) == 0:
                        logging.info("API counter at 0!")
                        sleep_epoch(answer.headers["X-RateLimit-Reset"])
                        answer = session.get(link_repo + str(commit_page), auth=(username, token))
                        time.sleep(0.72)

                if not skip:
                    if status == "200 OK":
                        done = True
                    else:
                        logging.error("Received unexpected answer while connecting with api.github.com:")
                        print(link_userinfo + cur_username)
                        print(answer.headers)
                        print(answer.text)
                        time.sleep(0.72)
                        cnt_triesGH += 1
                        if cnt_triesGH > 50:
                            logging.fatal("Too many failed GET requests without 200 OK:")
                            print(link_userinfo + cur_username)
                            print(answer.headers)
                            print(answer.text)
                            sys.exit()
            except Exception as e:
                logging.warning("Could not send GET request to api.github.com")
                print(e)
                time.sleep(0.72)
                cnt_triesGH += 1
                if cnt_triesGH > 50:
                    logging.critical("Too many failed GET requests. Waiting 60 min ...")
                    time.sleep(3600)
                elif cnt_triesGH > 70:
                    logging.fatal("Too many failed GET requests")
                    sys.exit()

        try:
            if int(answer.headers["X-RateLimit-Remaining"]) % 1000 == 0:
                logging.info("GitHub requests remaining: " + str(answer.headers["X-RateLimit-Remaining"]))
        except:
            pass
                
        if not skip:
            try:
                for contribution in answer.json():
                    # make sure that commit is performed by corresponding user
                    # (repos can be share by several users)
                    if contribution["author"]["login"] == cur_username:
                        queryresult[contribution["commit"]["date"]] = 0
            except Exception as e:
                logging.debug("Could not compute repo entries for: " + str(cur_username))
        else:
            logging.debug("Username not found: " + str(cur_username))
    try:        
        answer = answer.json()
    except:
        answer = ["_"]


logging.info("Storing data ...")
with open(path_results, "w") as fp:
    json.dump(queryresult, fp)



logging.info("Done.")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))