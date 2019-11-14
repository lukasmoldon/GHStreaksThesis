# ---------- IMPORT ------------
import logging
import datetime
import statsmodels.formula.api as smf
import pandas as pd
import numpy as np
# ------------------------------


# ---------- INPUT -------------
path_source = "/home/lmoldon/results/regressionData.csv"
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
showCorrMatrix = False
showCountUniqueValues = False
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
# ------------------------------



log_starttime = datetime.datetime.now()


rawData = pd.read_csv(path_source)
regressionData = rawData.drop(["userday", "sunday"], axis=1)

if showCorrMatrix:
    logging.info("Correleation matrix:")
    print(regressionData.corr())
    print()

if showCountUniqueValues:
    logging.info("Total unique values distibution:")
    print(rawData.groupby("contribution_that_day")["userday"].nunique())
    print(rawData.groupby("after_change")["userday"].nunique())
    print(rawData.groupby("current_streak")["userday"].nunique())
    print(rawData.groupby("monday")["userday"].nunique())
    print(rawData.groupby("tuesday")["userday"].nunique())
    print(rawData.groupby("wednesday")["userday"].nunique())
    print(rawData.groupby("thursday")["userday"].nunique())
    print(rawData.groupby("friday")["userday"].nunique())
    print(rawData.groupby("saturday")["userday"].nunique())
    print(rawData.groupby("sunday")["userday"].nunique())
    print()

logging.info("Logistic regression results: ")
logit = smf.logit("contribution_that_day ~ after_change +np.log(current_streak+.5) +after_change:np.log(current_streak+.5) +monday+tuesday+wednesday+thursday+friday+saturday", regressionData)
result = logit.fit()
result.summary()


log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))