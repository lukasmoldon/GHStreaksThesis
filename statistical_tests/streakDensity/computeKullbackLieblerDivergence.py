# ---------- IMPORT ------------
import logging
import datetime
import numpy as np
from scipy.stats import entropy
# ------------------------------


# ---------- INPUT -------------
#path_source_before = "/home/lmoldon/results/streakDensityValuesBEFORE_BIN10_MIN30.json"
#path_source_after = "/home/lmoldon/results/streakDensityValuesAFTER_BIN10_MIN30.json"
# ------------------------------


# ---------- OUTPUT ------------
# ------------------------------


# ---------- CONFIG ------------
numberEvents = 10 # = BIN
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
before = [
    0.1033273611619958, 
    0.10506704234192618, 
    0.10644564769177582, 
    0.10325183666955014, 
    0.10278136397892922, 
    0.10104508628566294, 
    0.09895238885451325, 
    0.09794866760403614, 
    0.09332557248561882, 
    0.08785503292599428
    ]

after = [
    0.09786552800347588, 
    0.10103126858777364, 
    0.10527192941848715, 
    0.10264437426873035, 
    0.1025429142385153, 
    0.10362483043090845, 
    0.1008958952193462, 
    0.10049383388434045, 
    0.09514056590970547, 
    0.09048886003872
]

uniform = np.full(numberEvents, 1/numberEvents)
# ------------------------------



# See https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence
def dkl(A, B):
    value = 0
    i = 0
    while i < len(A):
        value += (A[i] * np.log(A[i] / B[i]))
        i += 1
    return value

log_starttime = datetime.datetime.now()

logging.info("Scipy before = " + str(entropy(before, uniform)))
logging.info("DKL(B||Q) before = " + str(dkl(before, uniform)))
logging.info("DKL(Q||B) before = " + str(dkl(uniform, before)))
logging.info()
logging.info("Scipy after = " + str(entropy(after, uniform)))
logging.info("DKL(A||Q) after = " + str(dkl(after, uniform)))
logging.info("DKL(Q||A) after = " + str(dkl(uniform, after)))

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))