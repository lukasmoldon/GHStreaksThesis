# ---------- IMPORT ------------
import logging
import matplotlib
import matplotlib.pyplot as plt
import datetime
import json
import ijson
from datetime import timedelta, date
# ------------------------------


# ---------- INPUT -------------
path_source_streakdata = "/home/lmoldon/data/user_streaks.json"
path_source_usergroupsize = "/home/lmoldon/data/usergroupsize.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results_values = "/home/lmoldon/results/streakValues.json"
path_results_plot = "/home/lmoldon/results/streakPlot.png"
# ------------------------------


# ---------- CONFIG ------------
# Open a new window and show resulting plot? (only on desktop)
showplot = False
showdata = False  # Print plotdata?
savedata = True  # Save the resulting plot data at path_results_plot?
saveplotasimg = True  # Save the resulting plot as image file at path_results_plot?
showcoverage = True  # Show streak coverage?
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
plotdata = {}  # key = monday type, value = {key = day in observedtime, value = value}
start = date(1970, 1, 1)
end = date(1970, 1, 1)
# after this day everyone of observed usergroup joined GitHub
maxday_usergroupsize = date(1970, 1, 1)
# before this day nobody of observed usergroup joined GitHub
minday_usergroupsize = date(2099, 1, 1)
list_of_datetimes = []
values = []
cnt_streaks = 0  # total number of streaks
cnt_streaks_survived = 0  # number of streaks observed in plot
observedtime_start = date(2016, 4, 18)
observedtime_end = date(2016, 12, 31)
observed_mondays = [date(2016, 4, 18), date(2016, 4, 25), date(2016, 5, 2), date(2016, 5, 9), date(
    2016, 5, 16), date(2016, 5, 23), date(2016, 5, 30), date(2016, 6, 6), date(2016, 6, 13), date(2016, 6, 20)]
# ------------------------------


log_starttime = datetime.datetime.now()


def daterange(observedtime_start, observedtime_end):
    for n in range(int((observedtime_end - observedtime_start).days)):
        yield observedtime_start + timedelta(n)



monday_index = 0
while monday_index < len(observed_mondays):
    plotdata[str(monday_index)] = {}
    for single_date in daterange(observedtime_start, observedtime_end):
        plotdata[str(monday_index)][str(single_date.strftime("%Y-%m-%d"))] = 0
    monday_index += 1


logging.info("Accessing usergroupsize data ...")
with open(path_source_usergroupsize, "r") as fp:
    usergroupsize = json.load(fp)

for entry in usergroupsize:
    thisday = datetime.datetime.strptime(str(entry), datetimeFormat).date()
    if thisday > maxday_usergroupsize:
        maxday_usergroupsize = thisday
    if thisday < minday_usergroupsize:
        minday_usergroupsize = thisday

logging.info("Done. (1/3)")



logging.info("Starting ...")
streakdata = ijson.parse(open(path_source_streakdata, "r"))
for prefix, event, value in streakdata:
    if ".start" in prefix:
        start = datetime.datetime.strptime(str(value), datetimeFormat).date()
        cnt_streaks += 1
        if cnt_streaks % 1000000 == 0:
            logging.info(str(cnt_streaks/1000000) +
                         " million streaks computed.")
    elif ".end" in prefix:
        end = datetime.datetime.strptime(str(value), datetimeFormat).date()
    elif ".len" in prefix:
        if start in observed_mondays:
            monday_index = str(observed_mondays.index(start))
            if end <= observedtime_end:
                for single_date in daterange(start, end):
                    plotdata[monday_index][str(single_date)] += ((single_date - start) + timedelta(days=1)).days
            else:
                for single_date in daterange(start, observedtime_end):
                    plotdata[monday_index][str(single_date)] += ((single_date - start) + timedelta(days=1)).days

logging.info("Done. (2/3)")


logging.info("Creating plot ...")

for monday_index in plotdata:  # divide by usergroupsize
    for day in plotdata[monday_index]:
        thisday = datetime.datetime.strptime(str(day), datetimeFormat).date()
        if str(thisday) in usergroupsize:
            plotdata[monday_index][day] = (plotdata[monday_index][day] / usergroupsize[str(thisday)])
        elif thisday > maxday_usergroupsize:
            plotdata[monday_index][day] = (plotdata[monday_index][day] /
                            usergroupsize[str(maxday_usergroupsize)])
        elif thisday < minday_usergroupsize:
            del plotdata[monday_index][day]
        else:
            logging.critical("Error with date: " + str(thisday))
            del plotdata[monday_index][day]

for monday_index in plotdata:
    values = []
    list_of_datetimes = []

    for day in plotdata[monday_index]:
        list_of_datetimes.append(
            datetime.datetime.strptime(day, datetimeFormat).date())
        values.append(plotdata[monday_index][day])

    dates = matplotlib.dates.date2num(list_of_datetimes)
    matplotlib.pyplot.plot_date(dates, values, '-', label=str(observed_mondays[monday_index]))



plt.axvline(x=datetime.datetime.strptime(
    "2016-05-19", datetimeFormat).date(), color='r')
plt.xlabel("Time")
plt.ylabel("Avg. streak length")


if saveplotasimg:
    plt.savefig(path_results_plot, quality=100)
    logging.info("Plot image saved.")

if savedata:
    with open(path_results_values, "w") as fp:
        json.dump(plotdata, fp)
    logging.info("Plot data saved.")

if showdata:
    logging.info("Data:")
    print(plotdata)

if showplot:
    plt.show()

if showcoverage:
    logging.info("Streaks total: " + str(cnt_streaks))
    logging.info("Streaks in plot: " + str(cnt_streaks_survived))
    logging.info(str((cnt_streaks_survived / cnt_streaks) * 100) +
                 "%" + " coverage of reduced_users streaks in plot.")


logging.info("Done. (3/3)")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))
