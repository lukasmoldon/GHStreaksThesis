# ---------- IMPORT ------------
import logging
import ijson
# ------------------------------


# ---------- INPUT -------------
path_source = "C:/Users/Lukas/Desktop/Bachelorarbeit/code/data/user_streaks.json"
# ------------------------------


# ---------- OUTPUT ------------
path_results = ""
# ------------------------------


# ---------- CONFIG ------------
threshold = 10
time = 2016
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
streaks_ended = {}
streaks_ended_weighted = {}
# ------------------------------



jsonfile = ijson.parse(open(path_source, "r"))
cnt = 0
for prefix, event, value in jsonfile:
    if ".start" in prefix:
        start = str(value)
        cnt += 1
        if cnt % 1000000 == 0: logging.info(str(cnt/1000000) + " million streaks computed.")
    elif ".end" in prefix:
        end = str(value)
    if event == "number" and int(value) >= threshold and (str(time) in end):
        '''
        print("START: " + start)
        print("END: " + end)
        print("LENGTH: " + str(value))
        print("---------------------------")
        '''
        if end in streaks_ended:
            streaks_ended[end] += 1
            streaks_ended_weighted[end] += int(value)
        else:
            streaks_ended[end] = 1
            streaks_ended_weighted[end] = int(value)
        
    
print("------------- STREAKS ENDED: --------------")
print(streaks_ended)
print("--------- STREAKS ENDED Weighted: ---------")
print(streaks_ended_weighted)
print("-------------------------------------------")



'''
print(str(prefix) + "|" + str(event) + "|" + str(value))
    print("---------------------------------------------")
    cnt+=1
    if cnt > 200: break
'''

