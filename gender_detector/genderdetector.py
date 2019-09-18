# ---------- IMPORT ------------
import requests
import requests_html
import datetime
import json
import time
import logging
import gender_guesser.detector as gender
from geopy.geocoders import Nominatim
import sys
# ------------------------------


# ---------- INPUT -------------
path_source_userdata = "/home/lmoldon/data/users_reduced.json"
path_source_accepted_countries = "/home/lmoldon/data/gender_countries.json"
path_source_translate = "/home/lmoldon/data/translate.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/data/users_gender.json"
# ------------------------------


# ---------- CONFIG ------------
username = "XXXXXXXXXXXXXXXXXXXXX"
token = "XXXXXXXXXXXXXXXXXXXXX"
useragent = "Research for bachelor thesis on GitHub streaks"

cooldown_geolocate = 0.1 # How many seconds waiting if geolocate requests failed?
threshold_geolocate = 5 # How many tries for connecting with geopy before rejecting coordinates?
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
session = requests_html.HTMLSession()
gdetector = gender.Detector(case_sensitive=False)
geolocator = Nominatim(user_agent=useragent)

link_userinfo = "https://api.github.com/users/"
cnt_users = 0

userdata = {} # from reduced_users
genderdata = {} # "userID": {"name": "username", "gender":"m/f/mm/mf/a/u/e"}
stats = {
    "male": 0, # m
    "female": 0, # f
    "mostly_male": 0, # mm
    "mostly_female": 0, # mf
    "andy": 0, # a (androgynous)
    "unknown": 0, # u
    "error": 0 # e
}

# Dict of country names gender-guesser knows
accepted_countries = {}
# Translate geopy country names to gender-guesser country names
translate = {}
# ------------------------------



log_starttime = datetime.datetime.now()


def sleep_epoch(epochtime):
    start = datetime.datetime.fromtimestamp(int(epochtime) + 10)
    now = datetime.datetime.now().replace(microsecond=0)
    logging.info("Waiting for API counter reset in " + str(start - now))
    time.sleep((start - now).seconds)
    logging.info("Stopped waiting!")



def get_gender_by_coordinates(name, lat, lon):

    noGeo = False # if country locating fails, get gender without that information

    if lon < -180 or lon > 180 or lat < -90 or lat > 90 or lat == lon:
        logging.warning("Invalid coordinates for username: " + str(name) + ", with coordinates: " + str(lat) + ", " + str(lon))
        noGeo = True

    if not noGeo:
        cnt_tries = 0
        while(cnt_tries < threshold_geolocate):
            try:
                location = geolocator.reverse( (lat, lon), language="en")
                logging.debug(str(location.raw['address']['country']) + "Never delete this line!") # This is NOT a debug print - its for testing the result (string = country or None-type = e.g. ocean)
            except:
                cnt_tries += 1
                if cnt_tries == threshold_geolocate:
                    logging.critical("Could not get country for username: " + str(name) + ", with coordinates: " + str(lat) + ", " + str(lon))
                    noGeo = True
                else:
                    time.sleep(cooldown_geolocate)
            else:
                cnt_tries = threshold_geolocate

    if not noGeo:
        if str(location.raw['address']['country'].lower()) in accepted_countries:
            try:
                gender = gdetector.get_gender(name, str(location.raw['address']['country'].lower()))
            except:
                logging.critical("Failed to get gender with valid location for username " + str(name))
                return "ERROR"
        elif str(location.raw['address']['country']) in translate:
            try:
                gender = gdetector.get_gender(name, translate[str(location.raw['address']['country'])])
            except:
                logging.critical("Failed to get gender with translated location for username " + str(name))
                return "ERROR"
        else:
            try:
                gender = gdetector.get_gender(name)
                logging.debug("Following country unknown for gender-detection: " + str(location.raw['address']['country']))
            except:
                logging.critical("Failed to get gender without location but valid coordinates(!) for username " + str(name))
                return "ERROR"
    else:
        try:
            gender = gdetector.get_gender(name)
        except:
            logging.critical("Failed to get gender without location for username " + str(name))
            return "ERROR"
    
    return gender






logging.info("Loading data ...")

logging.info("Loading userdata ...")
with open(path_source_userdata, "r") as fp:
    userdata = json.load(fp)

logging.info("Loading accepted countries ...")
with open(path_source_accepted_countries, "r") as fp:
    accepted_countries = json.load(fp)

logging.info("Loading translator ...")
with open(path_source_translate, "r") as fp:
    translate = json.load(fp)

logging.info("Done.")




logging.info("Connecting with api.github.com ...")

answer = session.get(link_userinfo + "TheLukester", auth=(username, token))
status = answer.headers["Status"]
if status == "200 OK":
    logging.info(status)
elif int(answer.headers["X-RateLimit-Remaining"]) == 0:
    logging.warning("API counter at 0!")
    sleep_epoch(answer.headers["X-RateLimit-Reset"])
else:
    logging.error("Unexpected Error occurred while connecting with api.github.com:")
    print(answer.headers)
    print(answer.text)
    sys.exit()

logging.info("Done.")




for userid in userdata:
    cur_username = userdata[userid]["name"]
    cur_lat = float(userdata[userid]["lat"])
    cur_long = float(userdata[userid]["long"])

    answer = session.get(link_userinfo + cur_username, auth=(username, token))

    if status != "200 OK":
        if int(answer.headers["X-RateLimit-Remaining"]) == 0:
            logging.info("API counter at 0!")
            sleep_epoch(answer.headers["X-RateLimit-Reset"])
            answer = session.get(link_userinfo + cur_username, auth=(username, token))
        else:
            logging.error("Unexpected Error occurred while connecting with api.github.com:")
            print(answer.headers)
            print(answer.text)
            sys.exit()

    if status == "200 OK":
        if int(answer.headers["X-RateLimit-Remaining"]) % 1000 == 0:
            logging.info("Requests remaining: " + str(answer.headers["X-RateLimit-Remaining"]))
    else:
        logging.error("Unexpected Error occurred while connecting with api.github.com after waiting for counter reset:")
        print(answer.headers)
        print(answer.text)
        sys.exit()
        
    try:
        cur_fullname = answer.json()["name"]
        cur_firstname = cur_fullname.split()[0]
        cur_gender = get_gender_by_coordinates(cur_firstname, cur_lat, cur_long)
        if cur_gender != "ERROR":
            try:
                stats[str(cur_gender)] += 1
                genderdata[str(userid)] = {
                    "name": str(cur_fullname),
                    "gender": str(cur_gender)
                }
            except:
                logging.error("Could not save: " + str(cur_gender))
                stats["error"] += 1
        else:
            stats["error"] += 1
    except:
        logging.warning("Could not compute full name for username: " + str(cur_username))
    

    cnt_users += 1
    if cnt_users % 10000 == 0:
        logging.info("User count: " + str(cnt_users/1000) + "k")
        logging.info("Caching genderdata ...")

        with open(path_results, "w") as fp:
            json.dump(genderdata, fp)

        logging.info("Done.")

        logging.info("Meantime statistics:")
        sum = 0
        for entry in stats:
            sum += stats[entry]
            logging.info(str(entry) + ": " + str(stats[entry]))
        logging.info("Total: " + str(sum))




logging.info("Saving genderdata ...")

with open(path_results, "w") as fp:
    json.dump(genderdata, fp)

logging.info("Done.")

logging.info("Statistics:")
sum = 0
for entry in stats:
    sum += stats[entry]
    logging.info(str(entry) + ": " + str(stats[entry]))
logging.info("Total: " + str(sum))





logging.info("-------------- Done. --------------")
log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))