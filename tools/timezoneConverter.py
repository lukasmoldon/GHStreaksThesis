# ---------- IMPORT ------------
import logging
import datetime
from timezonefinderL import TimezoneFinder
import pytz
from pytz import common_timezones
from pytz import timezone
# ------------------------------


# ---------- INPUT -------------
usr_long = -78.78115845
usr_lat = 35.78974915
timestamp = "2012-03-29 22:17:03"
# ------------------------------


# ---------- OUTPUT ------------
path_results = ""
# ------------------------------


# ---------- CONFIG ------------
# for zone in common_timezones: print(zone) # get all known timezones
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
tf = TimezoneFinder()
datetimeFormat = "%Y-%m-%d %H:%M:%S"
start_workers = datetime.datetime.strptime("1900-01-01 09:00:00", datetimeFormat).time()
end_workers = datetime.datetime.strptime("1900-01-01 17:00:00", datetimeFormat).time()
standard_zone = timezone("UTC") # according to "Why do People Give Up Flossing? A Study of Contributor Disengagement in Open Source" GHTorrent only uses UTC as timezone
group = ""
# ------------------------------




if usr_long != 0 and usr_long <= 180 and usr_long >= -180 and usr_lat != 0 and usr_lat <= 90 and usr_lat >= -90:
    timestamp = datetime.datetime.strptime(timestamp, datetimeFormat) # convert timestamp in datetime format
    standard_time = standard_zone.localize(timestamp) # add timezone (UTC) to datetime format

    usr_zone = timezone(tf.timezone_at(lng=usr_long, lat=usr_lat)) # get timezone of the user
    usr_time = standard_time.astimezone(usr_zone) # convert UTC time to user timezone
    usr_time = usr_time.replace(tzinfo=None) # remove timezone tag for further operations

    if usr_time.time() >= start_workers and usr_time.time() <= end_workers and usr_time.weekday() < 5:
        group = "Working Hours"
    else:
        group = "Freetime"

    

logging.info("------------ Results: ------------")
logging.info("Users timezone: " + str(usr_zone))
logging.info("Users local time: " + str(usr_time))
logging.info("Users group: " + group)
logging.info("----------------------------------")