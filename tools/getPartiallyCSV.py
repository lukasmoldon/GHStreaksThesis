# ---------- IMPORT ------------
import pandas as pd
import logging
# ------------------------------


# ---------- INPUT -------------
path_source_users = "/home/johannes/data/github/mysql-2019-06-01/users.csv"
path_source_projects = "/home/johannes/data/github/mysql-2019-06-01/projects.csv"
path_source_commits = "/home/johannes/data/github/mysql-2019-06-01/commits.csv"
path_source_issues = "/home/johannes/data/github/mysql-2019-06-01/issues.csv"
path_source_project_commits = "/home/johannes/data/github/mysql-2019-06-01/project_commits.csv"
# ------------------------------


# ---------- OUTPUT ------------
path_results_users = "/home/lmoldon/data/csv/users_partially.csv"
path_results_projects = "/home/lmoldon/data/csv/projects_partially.csv"
path_results_commits = "/home/lmoldon/data/csv/commits_partially.csv"
path_results_issues = "/home/lmoldon/data/csv/issues_partially.csv"
path_results_project_commits = "/home/lmoldon/data/csv/project_commits_partially.csv"
# ------------------------------


# ---------- CONFIG ------------
amount = 10000 # how many rows (entries) per partially csv file?
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
# ------------------------------



logging.info("Starting ...")

# USERS
data = pd.read_csv(path_source_users, nrows=amount, header=None, delimiter=",", names=["id","name","company","created_at","type","fake","deleted","long","lat","country_code","county","city","region"])
data = data.set_index("id")
# data = data.drop([-1], axis=0) # corrupted(?) entry with not natural number id = "-1"
logging.info("Storing data ... (1/5)")
data.to_csv(path_results_users, encoding='utf-8', index="id")


# PROJECTS
data = pd.read_csv(path_source_projects, nrows=amount, header=None, delimiter=",", names=["id","url","owner_id","name","description","language","created_at","forked_from","deleted","updated_at","junk"])
data = data.set_index("id")
# data = data.drop([-1], axis=0) # corrupted(?) entry with not natural number id = "-1"
# data = data.drop(["junk"], axis=1) # not sure what this column is good for, not mentioned on GHTorrent
logging.info("Storing data ... (2/5)")
data.to_csv(path_results_projects, encoding='utf-8', index="id")


# COMMITS
data = pd.read_csv(path_source_commits, nrows=amount, header=None, delimiter=",", names=["id","sha","author_id","committer_id","project_id","created_at"])
data = data.set_index("id")
# data = data.drop([1], axis=0) # corrupted(?) entry with not natural number id = "1.2"
logging.info("Storing data ... (3/5)")
data.to_csv(path_results_commits, encoding='utf-8', index="id")


# ISSUES
data = pd.read_csv(path_source_issues, nrows=amount, header=None, delimiter=",", names=["id","repo_id","reporter_id","assignee_id","pull_request","pull_request_id","created_at","issue_id"])
data = data.set_index("id")
# TODO anything to fix?
logging.info("Storing data ... (4/5)")
data.to_csv(path_results_issues, encoding='utf-8', index="id")


# PROJECT_COMMITS
data = pd.read_csv(path_source_project_commits, nrows=amount, header=None, delimiter=",", names=["project_id","commit_id"])
# TODO anything to fix?
logging.info("Storing data ... (5/5)")
data.to_csv(path_results_project_commits, encoding='utf-8', index=False)

logging.info("Done.")
