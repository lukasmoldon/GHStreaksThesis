'''
data = pd.read_csv(path, nrows=10)
data = pd.read_csv(path, header=None, delimiter=",", names=["id","name","company","created_at","type","fake","deleted","long","lat","country_code","county","city","region"])
data = pd.read_csv(path, index_col="id")

data = data.set_index("id")

data = data.drop([-1], axis=0)
data = data.drop(["name","company","created_at","type","fake","deleted","long","lat","country_code","county","city","region"], axis=1)

data.insert(0, "number_commits", 0, allow_duplicates = False) 

print(data)
print(data.loc[0])
print(data.loc[0].values)
print(data.loc[0].tolist())
print(data.loc[0]["B"])

data.to_csv("/home/lmoldon/data/users_partially.csv", encoding='utf-8', index=False)
data.to_csv(path, encoding='utf-8', index="id")

chunk = []
for row in chunk:
    print(row[0]) # ID
    print(row[0]) # content without ID
    print(row[1][0]) # first attribute (eg. users => name)
    print(row[1]["type"]) # "type" attribute

    user_id=0
    print(data.loc[user_id]["number_commits"]) # find number_commits entry at user_id
    break

# -----------------------

data = pd.DataFrame(columns=["id","number_commits"])
data.to_csv(path, encoding='utf-8', index=False)

data = pd.read_csv(path, index_col="id")
data = data.append({"id": "1", "number_commits": 1}, ignore_index=True)
data = data.set_index("id")
data.to_csv(path, encoding='utf-8')

data = pd.read_csv(path)
data = data.append({"id": "2", "number_commits": 1}, ignore_index=True)
data = data.set_index("id")
data.to_csv(path, encoding='utf-8')

data = pd.read_csv(path)
data = data.set_index("id")
data.loc[2]["number_commits"] += 1
data.to_csv(path, encoding='utf-8')

#------------------------

with open(path, "w") as fp:
    json.dump(data, fp)

with open(path, "r") as fp:
    data = json.load(fp)

#------------------------

datetimeFormat = "%Y-%m-%d %H:%M:%S"
removaldate = "2016-05-19 12:00:00"
x = datetime.datetime.strptime(removaldate, datetimeFormat)
print(x.date())

'''