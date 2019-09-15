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
path_source_groupdata = "/home/lmoldon/data/user_groups.json"
path_source_usergroupsize = "/home/lmoldon/data/usergroupsize.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results_values = "/home/lmoldon/results/streakValues.json"
path_results_plot = "/home/lmoldon/results/streakPlot.png"
# ------------------------------


# ---------- CONFIG ------------
threshold = 50 # minimum streak length to get plotted
showplot = False # Open a new window and show resulting plot? (only on desktop)
showdata = False # Print plotdata?
savedata = True # Save the resulting plot data at path_results_plot?
saveplotasimg = False # Save the resulting plot as image file at path_results_plot?
showcoverage = True # Show streak coverage?
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
datetimeFormat = "%Y-%m-%d"
plotdata = {} # key = day in observedtime, value = value of selected mode
start = date(1970, 1, 1)
end = date(1970, 1, 1)
maxday_usergroupsize = date(1970, 1, 1) # after this day everyone of observed usergroup joined GitHub
minday_usergroupsize = date(2099, 1, 1) # before this day nobody of observed usergroup joined GitHub
list_of_datetimes = []
values = []
cnt_streaks = 0 # total number of streaks
cnt_streaks_survived = 0 # number of streaks observed in plot
# ------------------------------

# TODO: Code