# ---------- IMPORT ------------
import datetime
import json
from timezonefinderL import TimezoneFinder
import pytz
from pytz import common_timezones
from pytz import timezone
import ijson
import logging
from datetime import timedelta
# ------------------------------


# ---------- INPUT -------------
path_source_dates_per_user = "/home/lmoldon/data/contribution_per_user.json"
path_source_userdata = "/home/lmoldon/data/users_reduced.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/data/contributions_per_user_per_day.json"
# ------------------------------


# ---------- CONFIG ------------
datetimeFormat = "%Y-%m-%d %H:%M:%S"
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
contributions = {} # key = userID, value = {"day1": 3, "day2": 1, ...})
userdata = {} # for location (timezone)
tf = TimezoneFinder()
singleday = datetime.timedelta(days=1)
standard_zone = timezone("UTC") # according to "Why do People Give Up Flossing? A Study of Contributor Disengagement in Open Source" GHTorrent only uses UTC as timezone
# ------------------------------



log_starttime = datetime.datetime.now()

logging.info("Accessing userdata ...")
with open(path_source_userdata, "r") as fp:
    userdata = json.load(fp)

logging.info("Done. (1/3)")


logging.info("Starting ...")
cur_usr_id = -1

jsonfile = ijson.parse(open(path_source_dates_per_user, "r"))
cnt = 0
for prefix, event, value in jsonfile:
    if prefix == "" and event == "map_key":
        # new user dict found
        cur_usr_id = value
        cur_usr_lat = float(userdata[str(cur_usr_id)]["lat"])
        cur_usr_long = float(userdata[str(cur_usr_id)]["long"])
        cur_usr_dates = {}

    elif prefix == cur_usr_id and event == "map_key":
        # value = new date of cur user
        try:
            timestamp_utc = datetime.datetime.strptime(value, datetimeFormat) # convert timestamp to datetime format
            timestamp_utc = standard_zone.localize(timestamp_utc) # add timezone (UTC) to datetime format
            usr_zone = timezone(tf.timezone_at(lng=cur_usr_long, lat=cur_usr_lat)) # get timezone of the user
            usr_time = timestamp_utc.astimezone(usr_zone) # convert UTC time to user timezone
            usr_time = usr_time.replace(tzinfo=None) # remove timezone tag for further operations (comparison)
            # date only: add to dict
            date = usr_time.date()
            if not (str(date) in cur_usr_dates):
                cur_usr_dates[str(date)] = 1
            else:
                cur_usr_dates[str(date)] += 1
        except:
            pass

    elif prefix == cur_usr_id and event == "end_map":
        # end of user dict
        contributions[str(cur_usr_id)] = cur_usr_dates
        cnt += 1
        if cnt % 100 == 0: 
            logging.info(str(cnt) + " users computed.")
        
logging.info("Done. (2/3)")


# save results
logging.info("Saving results ...")

with open(path_results, "w") as fp:
    json.dump(contributions, fp)

logging.info("Done. (3/3)")


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))
