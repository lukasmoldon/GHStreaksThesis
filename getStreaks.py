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
import bisect 
# ------------------------------


# ---------- INPUT -------------
path_source_dates_per_user = "/home/lmoldon/data/contribution_per_user.json"
path_source_userdata = "/home/lmoldon/data/users_reduced.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results_streakdata = "/home/lmoldon/data/user_streaks.json"
path_results_groupdata = "/home/lmoldon/data/user_groups.json"
# ------------------------------


# ---------- CONFIG ------------
datetimeFormat = "%Y-%m-%d %H:%M:%S"
start_workers = datetime.datetime.strptime("1900-01-01 09:00:00", datetimeFormat).time()
end_workers = datetime.datetime.strptime("1900-01-01 17:00:00", datetimeFormat).time()
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
streaks = {} # key = userID, value = {1: {"start": date, "end": date, "len": int}, ...}
usergroups = {} # key = userID, value = 0 (freetime) or value = 1 (worker)
userdata = {} # for location (timezone)
valid_users = 0 # how many users have valid date data?
tf = TimezoneFinder()
singleday = datetime.timedelta(days=1)
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
        cur_usr_freetime = 0
        cur_usr_worktime = 0
        cur_usr_dates = []

    elif prefix == cur_usr_id and event == "map_key":
        # value = new date of cur user
        try:
            timestamp_utc = datetime.datetime.strptime(value, datetimeFormat) # convert timestamp to datetime format
            timestamp_utc = standard_zone.localize(timestamp_utc) # add timezone (UTC) to datetime format
            usr_zone = timezone(tf.timezone_at(lng=cur_usr_long, lat=cur_usr_lat)) # get timezone of the user
            usr_time = timestamp_utc.astimezone(usr_zone) # convert UTC time to user timezone
            usr_time = usr_time.replace(tzinfo=None) # remove timezone tag for further operations (comparison)
            # work or freetime?
            if usr_time.time() >= start_workers and usr_time.time() <= end_workers and usr_time.weekday() < 5:
                cur_usr_worktime += 1
            else:
                cur_usr_freetime += 1
            # date only: add to array (sorted)
            date = usr_time.date()
            if not (date in cur_usr_dates):
                bisect.insort(cur_usr_dates, date)
        except:
            pass

    elif prefix == cur_usr_id and event == "end_map":
        # end of user dict => compute streaks/workingORfreetime/save
        cnt += 1
        if cnt % 100 == 0: 
            logging.info(str(cnt) + " users computed.")
        # streaks
        if cur_usr_dates != []:
            cur_usr_streaks = {}
            cur_usr_streakcnt = 1
            date_i = cur_usr_dates[0]
            cur_usr_streaks[cur_usr_streakcnt] = {
                "start": str(date_i),
                "end": str(date_i),
                "len": 1
            }
            i = 0
            while i < len(cur_usr_dates)-1:
                date_i = cur_usr_dates[i]
                date_ii = cur_usr_dates[i+1]
                if date_i + singleday == date_ii:
                    cur_usr_streaks[cur_usr_streakcnt]["end"] = str(date_ii) # expand end date of streak by one day
                    cur_usr_streaks[cur_usr_streakcnt]["len"] += 1 # increment lenght of streak by one day
                else:
                    cur_usr_streakcnt += 1 # save new streak with length 1
                    cur_usr_streaks[cur_usr_streakcnt] = {
                        "start": str(date_ii),
                        "end": str(date_ii),
                        "len": 1
                    }
                i += 1
            # only if cur_usr_streaks has content
            if cur_usr_streaks != []: 
                valid_users += 1
                streaks[cur_usr_id] = cur_usr_streaks
                # save number of contributions for both usergroups
                usergroups[cur_usr_id] = {"f": cur_usr_freetime, "w": cur_usr_worktime}
            else:
                logging.warning("No streaks survived of user with ID " + str(cur_usr_id))
        else:
            logging.warning("User with ID " + str(cur_usr_id) + " has no valid contribution data!")
        

# save streaks
with open(path_results_streakdata, "w") as fp:
    json.dump(streaks, fp)

# save usergroups
with open(path_results_groupdata, "w") as fp:
    json.dump(usergroups, fp)


logging.info("Users survived:" + str(valid_users))
logging.info("Done. (2/2)")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))
