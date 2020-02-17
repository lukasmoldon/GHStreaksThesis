# ---------- IMPORT ------------
import logging
import datetime
import json
import networkx as nx
import matplotlib.pyplot as plt
# ------------------------------


# ---------- INPUT -------------
path_source = "C:/Users/Lukas/Desktop/mutualFriends.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = ""
# ------------------------------


# ---------- CONFIG ------------

# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
# ------------------------------



log_starttime = datetime.datetime.now()


logging.info("Loading data ...")
with open(path_source, "r") as fp:
    data = json.load(fp)
logging.info("Done (1/2)")


logging.info("Starting ... ")

G = nx.Graph()

for firstnode in data:
    for secondnode in data[firstnode]:
        G.add_edge(firstnode, secondnode)

print("Number of nodes:", len(G.nodes()))
print("Number of links:", len(G.edges()))

L=len(G.edges())
N=len(G.nodes())
density=(2*L)/(N*(N-1))
print("Density:", density)

maxid="2"
cnt=0
for cnt in G.nodes:
    if G.degree[maxid] < G.degree[cnt]:
        maxid = cnt
print("Highest degree:", G.degree[maxid])

cnt = 0
giant = []
for c in nx.connected_components(G):
    cnt += 1
    if len(giant) < len(c):
        giant = c
print("Number of components:", cnt)
print("Nodes in giant component:", len(giant))
print("Nodes not in giant component:", len(G.nodes())-len(giant))

GC = G.copy()
for node in G.nodes():
    if node not in giant:
        GC.remove_node(node)

#print("Diameter of the network:", nx.diameter(GC))
#print("Average distance between nodes:", nx.average_shortest_path_length(GC))

y = [el/len(G.nodes()) for el in nx.degree_histogram(G)]
x = range(len(y))
plt.scatter(x, y)
plt.xlabel('degree')
plt.ylabel('p')
plt.show()

logging.info("Done (2/2)")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))