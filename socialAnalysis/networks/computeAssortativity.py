# ---------- IMPORT ------------
import logging
import datetime
import json
import networkx as nx
import random
import numpy as np
import math
# ------------------------------


# ---------- INPUT -------------
path_source_edges = "/home/lmoldon/data/mutualFriends.json"
path_source_attributes ="/home/lmoldon/data/maximumStreak.json"
# ------------------------------


# ---------- OUTPUT ------------

# ------------------------------


# ---------- CONFIG ------------
# corresponds to "t-1" in thesis (record > t-1 => streaker) 
streakerThreshold = 7
samplesize = 1000 # only for random model (avg)
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
# ------------------------------



log_starttime = datetime.datetime.now()


logging.info("Loading data ...")
with open(path_source_edges, "r") as fp:
    data_edges = json.load(fp)
with open(path_source_attributes, "r") as fp:
    data_attributes = json.load(fp)
logging.info("Done (1/2)")


logging.info("Starting ... ")

G = nx.Graph() # real empirical graph

ids = list(data_attributes.keys())

logging.info("Adding nodes ... ")
for userid in data_attributes:
    if data_attributes[userid] > streakerThreshold:
        G.add_node(userid, streaker="yes")
    else:
        G.add_node(userid, streaker="no")

logging.info("Adding edges ... ")
for firstnode in data_edges:
    for secondnode in data_edges[firstnode]:
        if firstnode in G.nodes() and secondnode in G.nodes():
            G.add_edge(firstnode, secondnode)

logging.info("Computing random model ... ")
coeff = []
p = []
i = 1
while i <= samplesize:
    R = nx.Graph() # same graph with attributes shuffled attribute values
    for userid in data_attributes:
        if data_attributes[random.choice(ids)] > streakerThreshold:
            R.add_node(userid, streaker="yes")
        else:
            R.add_node(userid, streaker="no")
    for firstnode in data_edges:
        for secondnode in data_edges[firstnode]:
            if firstnode in G.nodes() and secondnode in G.nodes():
                R.add_edge(firstnode, secondnode)
    coeff.append(nx.attribute_assortativity_coefficient(R,"streaker"))

    streaker_attr = nx.get_node_attributes(R, "streaker")
    cnt_pos = 0
    cnt_neg = 0
    for node in R.nodes():
        if streaker_attr[node] == "yes":
            found = False
            for neighbor in R.neighbors(node):
                if streaker_attr[neighbor] == "yes":
                    found = True
            if found:
                cnt_pos += 1
            else:
                cnt_neg += 1
    p.append(cnt_pos/(cnt_neg+cnt_pos))

    if i%10==0: 
        logging.info(str(i) + " random graphs computed")
    i += 1

avg = np.mean(coeff)
real = nx.attribute_assortativity_coefficient(G,"streaker")

stddeviation = 0
for value in coeff:
    stddeviation += ((value - avg) ** 2)
stddeviation = math.sqrt(stddeviation / samplesize)

zscore = 0
if stddeviation != 0:
    zscore = ((real - avg) / stddeviation)

logging.info("Computing ... ")
logging.info("Real assortativity coefficient: " +  str(real))
logging.info("Shuffled assortativity coefficient (avg): " +  str(avg))
logging.info("zScore assortativity: " +  str(zscore))


streaker_attr = nx.get_node_attributes(G, "streaker")
cnt_pos = 0
cnt_neg = 0
for node in G.nodes():
    if streaker_attr[node] == "yes":
        found = False
        for neighbor in G.neighbors(node):
            if streaker_attr[neighbor] == "yes":
                found = True
        if found:
            cnt_pos += 1
        else:
            cnt_neg += 1

logging.info("Real: P(n has streaking neighbor | n is streaker) = " + str(cnt_pos/(cnt_neg+cnt_pos)))
logging.info("Shuffled (avg): P(n has streaking neighbor | n is streaker) = " + str(np.mean(p)))


logging.info("Done (2/2)")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))