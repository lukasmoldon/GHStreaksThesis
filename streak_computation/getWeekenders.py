# ---------- IMPORT ------------
import datetime
import json
from timezonefinderL import TimezoneFinder
import pytz
from pytz import common_timezones
from pytz import timezone
import ijson
import logging
# ------------------------------


# ---------- INPUT -------------
path_source_dates_per_user = "/home/lmoldon/data/contribution_per_user.json"
path_source_userdata = "/home/lmoldon/data/users_reduced.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = "/home/lmoldon/data/weekenders.json"
# ------------------------------


# ---------- CONFIG ------------
datetimeFormat = "%Y-%m-%d %H:%M:%S"
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
usergroups = {} # key = userID, value = {"f": cur_usr_freetime, "w": cur_usr_worktime}
userdata = {} # for location (timezone)
tf = TimezoneFinder()
valid_users = 0
standard_zone = timezone("UTC") # according to "Why do People Give Up Flossing? A Study of Contributor Disengagement in Open Source" GHTorrent only uses UTC as timezone
# ------------------------------



log_starttime = datetime.datetime.now()

logging.info("Accessing userdata ...")
with open(path_source_userdata, "r") as fp:
    userdata = json.load(fp)

logging.info("Done. (1/2)")


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
        cur_usr_weekdays = 0
        cur_usr_weekend = 0

    elif prefix == cur_usr_id and event == "map_key":
        # value = new date of cur user
        try:
            timestamp_utc = datetime.datetime.strptime(value, datetimeFormat) # convert timestamp to datetime format
            timestamp_utc = standard_zone.localize(timestamp_utc) # add timezone (UTC) to datetime format
            usr_zone = timezone(tf.timezone_at(lng=cur_usr_long, lat=cur_usr_lat)) # get timezone of the user
            usr_time = timestamp_utc.astimezone(usr_zone) # convert UTC time to user timezone
            usr_time = usr_time.replace(tzinfo=None) # remove timezone tag for further operations (comparison)
            # work or freetime?
            if usr_time.weekday() < 5:
                cur_usr_weekdays += 1
            else:
                cur_usr_weekend += 1
        except:
            pass

    elif prefix == cur_usr_id and event == "end_map":
        # end of user dict => compute streaks/workingORfreetime/save
        cnt += 1
        if cnt % 1000 == 0: 
            logging.info(str(int(cnt/1000)) + " thousand users computed.")
        # only if cur_usr_streaks has content
        if cur_usr_weekdays != 0 or cur_usr_weekdays != 0: 
            valid_users += 1
            # save number of contributions for weekdays "WD" and weekends "WE"
            usergroups[str(cur_usr_id)] = {"WD": cur_usr_weekdays, "WE": cur_usr_weekend}
        else:
            logging.warning("No valid contribution data for user with ID: " + str(cur_usr_id))
        

# save results
with open(path_results, "w") as fp:
    json.dump(usergroups, fp)


logging.info("Users survived:" + str(valid_users))
logging.info("Done. (2/2)")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))
