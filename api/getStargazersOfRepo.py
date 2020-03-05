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
path_results = "/home/lmoldon/results/100DaysSTARGAZERS.json"
# ------------------------------


# ---------- CONFIG ------------
username = "XXXXXXXXXXXXXXXXXXXXX"
token = "XXXXXXXXXXXXXXXXXXXXX"
email = "XXXXXXXXXXXXXXXXXXXXX"
useragent = "Research for bachelor thesis on GitHub streaks"

collection_link_repo = {
    "0": "https://api.github.com/repos/kallaway/100-days-of-code",
    "1": "https://api.github.com/repos/harinij/100DaysOfCode",
    "2": "https://api.github.com/repos/harunshimanto/100-Days-Of-ML-Code",
    "3": "https://api.github.com/repos/Avik-Jain/100-Days-Of-ML-Code",
    "4": "https://api.github.com/repos/coells/100days",
    "5": "https://api.github.com/repos/talkpython/100daysofcode-with-python-course",
    "6": "https://api.github.com/repos/harshitahluwalia7895/100DaysOfMLCode",
    "7": "https://api.github.com/repos/xandeer/100-days-of-code",
    "8": "https://api.github.com/repos/twostraws/100",
    "9": "https://api.github.com/repos/karakarakaraff/100-days-of-code",
    "10": "https://api.github.com/repos/CypherPoet/100-days-of-swiftui-and-combine",
    "11": "https://api.github.com/repos/fnplus/100DaysOfCode",
    "12": "https://api.github.com/repos/jangidkrishna/100_days_of_algo",
    "13": "https://api.github.com/repos/mimukit/100-days-of-code-log",
    "14": "https://api.github.com/repos/shafayeatsumit/100_days_of_algo",
    "15": "https://api.github.com/repos/Sabbir1996/100-Days-Of-Code",
    "16": "https://api.github.com/repos/SeshanPillay25/100-days-of-code",
    "17": "https://api.github.com/repos/akashgiricse/100DaysOfML",
    "18": "https://api.github.com/repos/EduApps-CDG/100DaysOfCode",
    "19": "https://api.github.com/repos/rowmatrix/100-days-of-code",
    "20": "https://api.github.com/repos/jhrcook/100DaysOfSwift",
    "21": "https://api.github.com/repos/subhashb/100-days-of-ml",
    "22": "https://api.github.com/repos/Jeet1994/100DaysOfCode",
    "23": "https://api.github.com/repos/bapspatil/100ishDaysOfCode",
    "24": "https://api.github.com/repos/TarangRanpara/100-days-of-coding-challenge",
    "25": "https://api.github.com/repos/gjergjk71/100Days-Python-Challenge",
    "26": "https://api.github.com/repos/Avi-1996/100-Days-Code-Challenge",
    "27": "https://api.github.com/repos/wenyizag/CSS-100-Day-Challenge",
    "28": "https://api.github.com/repos/kateamethyst/100DaysCSSChallenge",
    "29": "https://api.github.com/repos/dashcroft/100-days-of-code"
    }
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
data = {}
userdata = {}
link_userinfo = "https://api.github.com/users/"

link_repo_tail = "/stargazers?per_page=100&page="

useragent = useragent + "  Contact: " + email
session = requests_html.HTMLSession()

cnt_users = 0
cnt_identified = 0
# ------------------------------


def sleep_epoch(epochtime):
    start = datetime.datetime.fromtimestamp(int(epochtime) + 10)
    now = datetime.datetime.now().replace(microsecond=0)
    logging.info("Waiting for API counter reset in " + str(start - now))
    time.sleep((start - now).seconds)
    logging.info("Stopped waiting!")

def getUserIdFromLogin(login):
    for userID in userdata:
        if userdata[userID]["name"] == login:
            return userID
    return -1


log_starttime = datetime.datetime.now()


logging.info("Loading data ...")
with open(path_source_userdata, "r") as fp:
    userdata = json.load(fp)
logging.info("Done (1/3)")


logging.info("Starting...")

logging.info("Connecting with api.github.com:")

cnt_triesGH = 0
done = False
while(not done):
    try:
        answer = session.get(link_userinfo + "lukasmoldon", auth=(username, token))

        status = answer.headers["Status"]
        if status != "200 OK":
            if int(answer.headers["X-RateLimit-Remaining"]) == 0:
                logging.info("API counter at 0!")
                sleep_epoch(answer.headers["X-RateLimit-Reset"])
                answer = session.get(link_userinfo + "lukasmoldon", auth=(username, token))

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
    except:
        logging.warning("Could not send GET request to api.github.com")
        time.sleep(0.72)
        cnt_triesGH += 1
        if cnt_triesGH > 50:
            logging.fatal("Too many failed GET requests")
            sys.exit()

logging.info("Done.")


logging.info("Starting ...")

for index in collection_link_repo:

    link_repo = collection_link_repo[index] + link_repo_tail

    done = False
    page = 1
    while(not done):
        try:
            answer = session.get(link_repo + str(page), auth=(username, token))

            status = answer.headers["Status"]
            if status != "200 OK":
                if int(answer.headers["X-RateLimit-Remaining"]) == 0:
                    logging.info("API counter at 0!")
                    sleep_epoch(answer.headers["X-RateLimit-Reset"])
                    answer = session.get(link_repo + str(page), auth=(username, token))

                if status == "200 OK":
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

            stargazer = answer.json()
            if len(stargazer) > 0:
                for cur_user_data in stargazer:
                    cnt_users += 1
                    if cnt_users % 100 == 0:
                        logging.info(str(cnt_users) + " users computed")
                    usersearch = getUserIdFromLogin(cur_user_data["login"])
                    if usersearch != -1:
                        cnt_identified += 1
                        data[str(usersearch)] = cur_user_data["login"]
                page += 1
                time.sleep(0.72)
            else:
                done = True
        except:
            logging.warning("Could not send GET request to api.github.com")
            time.sleep(0.72)
            cnt_triesGH += 1
            if cnt_triesGH > 50:
                logging.fatal("Too many failed GET requests")
                sys.exit()

logging.info("Done. (2/3)")


logging.info("Saving results ...")
with open(path_results, "w") as fp:
    json.dump(data, fp)
logging.info("Done. (3/3)")

logging.info("Total number of users: " + str(cnt_users))
logging.info("Total number of identified users: " +  str(cnt_identified))

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))