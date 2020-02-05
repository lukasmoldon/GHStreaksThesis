# ---------- IMPORT ------------
import pandas as pd
import logging
import datetime
# ------------------------------


# ---------- INPUT -------------
path_source_users = "/home/johannes/data/github/mysql-2019-06-01/users.csv"
path_source_projects = "/home/johannes/data/github/mysql-2019-06-01/projects.csv"
path_source_commits = "/home/johannes/data/github/mysql-2019-06-01/commits.csv"
path_source_issues = "/home/johannes/data/github/mysql-2019-06-01/issues.csv"
path_source_project_commits = "/home/johannes/data/github/mysql-2019-06-01/project_commits.csv"
path_source_commit_comments = "/home/johannes/data/github/mysql-2019-06-01/commit_comments.csv"
path_source_pull_request_comments = "/home/johannes/data/github/mysql-2019-06-01/pull_request_comments.csv"
path_source_issue_comments = "/home/johannes/data/github/mysql-2019-06-01/issue_comments.csv"
# ------------------------------


# ---------- OUTPUT ------------
path_results_users = "/home/lmoldon/data/csv/users_partially.csv"
path_results_projects = "/home/lmoldon/data/csv/projects_partially.csv"
path_results_commits = "/home/lmoldon/data/csv/commits_partially.csv"
path_results_issues = "/home/lmoldon/data/csv/issues_partially.csv"
path_results_project_commits = "/home/lmoldon/data/csv/project_commits_partially.csv"
path_results_commit_comments = "/home/lmoldon/data/csv/commit_comments_partially.csv"
path_results_pull_request_comments = "/home/lmoldon/data/csv/pull_request_comments_partially.csv"
path_results_issue_comments = "/home/lmoldon/data/csv/issue_comments_partially.csv"
# ------------------------------


# ---------- CONFIG ------------
amount = 10000 # how many rows (entries) per partially csv file?
# ------------------------------


# ---------- INITIAL -----------
logging.basicConfig(format='%(asctime)s [%(levelname)s] - %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=logging.INFO)
# ------------------------------



log_starttime = datetime.datetime.now()

logging.info("Starting ...")

# USERS
data = pd.read_csv(path_source_users, nrows=amount, header=None, delimiter=",", names=["id","name","company","created_at","type","fake","deleted","long","lat","country_code","county","city","region"])
data = data.set_index("id")
# data = data.drop([-1], axis=0) # corrupted(?) entry with not natural number id = "-1"
logging.info("Storing data ... (1/8)")
data.to_csv(path_results_users, encoding='utf-8', index="id")


# PROJECTS
data = pd.read_csv(path_source_projects, nrows=amount, header=None, delimiter=",", names=["id","url","owner_id","name","description","language","created_at","forked_from","deleted","updated_at","junk"])
data = data.set_index("id")
# data = data.drop([-1], axis=0) # corrupted(?) entry with not natural number id = "-1"
# data = data.drop(["junk"], axis=1) # not sure what this column is good for, not mentioned on GHTorrent
logging.info("Storing data ... (2/8)")
data.to_csv(path_results_projects, encoding='utf-8', index="id")


# COMMITS
data = pd.read_csv(path_source_commits, nrows=amount, header=None, delimiter=",", names=["id","sha","author_id","committer_id","project_id","created_at"])
data = data.set_index("id")
# data = data.drop([1], axis=0) # corrupted(?) entry with not natural number id = "1.2"
logging.info("Storing data ... (3/8)")
data.to_csv(path_results_commits, encoding='utf-8', index="id")


# ISSUES
data = pd.read_csv(path_source_issues, nrows=amount, header=None, delimiter=",", names=["id","repo_id","reporter_id","assignee_id","pull_request","pull_request_id","created_at","issue_id"])
data = data.set_index("id")
logging.info("Storing data ... (4/8)")
data.to_csv(path_results_issues, encoding='utf-8', index="id")


# PROJECT_COMMITS
data = pd.read_csv(path_source_project_commits, nrows=amount, header=None, delimiter=",", names=["project_id","commit_id"])
logging.info("Storing data ... (5/8)")
data.to_csv(path_results_project_commits, encoding='utf-8', index=False)


# COMMIT COMMENTS
data = pd.read_csv(path_source_commit_comments, nrows=amount, header=None, delimiter=",", names=["id","commit_id", "user_id", "body", "line", "position", "comment_id", "created_at"])
logging.info("Storing data ... (6/8)")
data.to_csv(path_results_commit_comments, encoding='utf-8', index=False)


# PULL REQUEST COMMENTS
data = pd.read_csv(path_source_pull_request_comments, nrows=amount, header=None, delimiter=",", names=["pull_request_id","user_id", "comment_id", "position", "body", "commit_id", "created_at"])
logging.info("Storing data ... (7/8)")
data.to_csv(path_results_pull_request_comments, encoding='utf-8', index=False)


# ISSUE COMMENTS
data = pd.read_csv(path_source_issue_comments, nrows=amount, header=None, delimiter=",", names=["issue_id","user_id", "comment_id", "created_at"])
logging.info("Storing data ... (8/8)")
data.to_csv(path_results_issue_comments, encoding='utf-8', index=False)



logging.info("Done.")

log_endtime = datetime.datetime.now()
log_runtime = (log_endtime - log_starttime)
logging.info("Total runtime: " + str(log_runtime))
