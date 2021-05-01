## Introduction
This repository provides the code for "*How Gamification Affects Software Developers: Cautionary Evidence from a Natural Experiment on GitHub*" appearing in ICSE 2021 and my bachelor thesis "*Sending signals in open source: Evidence from a natural experiment*". The project uses the [GHTorrent MySQL database from June 2019](https://ghtorrent.org/downloads.html). We examine how the behavior of software developers changes in response to removing gamification elements from GitHub, an online platform for collaborative programming and software development. We find that the unannounced removal of daily activity streak counters from the user interface (from user profile pages) was followed by significant changes in behavior. Long-running streaks of activity were abandoned and became less common. Weekend activity decreased and days in which developers made a single contribution became less common. Synchronization of streaking behavior in the platform's social network also decreased, suggesting that gamification is a powerful channel for social influence. Focusing on a set of software developers that were publicly pursuing a goal to make contributions for 100 days in a row, we find that some of these developers abandon this quest following the removal of the public streak counter. Our findings provide evidence for the significant impact of gamification on the behavior of developers on large collaborative programming and software development platforms. They urge caution: gamification can steer the behavior of software developers in unexpected and unwanted directions.


--- 
* The ICSE paper (11 pages) is available [>>here<<](https://www.computer.org/csdl/proceedings-article/icse/2021/029600a549/1sEXoczR0TC) .
* The arxiv preprint (11 pages) is available [>>here<<](https://arxiv.org/abs/2006.02371) .
* The thesis paper (50 pages) is available [>>here<<](https://johanneswachs.com/papers/BachelorMoldon.pdf) .
---


## How to use
The project consists of different directories, which get described below. All scripts either use the raw csv data from GHTorrent or previous computed json/csv files by other files. At the beginning of each script there exists an *INPUT* section which includes the paths for all required files for the computation and an *OUTPUT* section for the corresponding resulting files with their paths. Running scripts from the **api** folder requires a [personal access token for the GitHub API](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token), the corresponding credentials can be inserted in the *CONFIG* section of each api file.

## Data
The most important data sets are [available on Zenodo](https://zenodo.org/record/4710603#.YI0lFaGxWUk). Please note that the file *"commits_reduced.json"* is not part of this data set due to its large size and Zenodo's file size limit of 50GB. Alternatively you can use the [GHTorrent MySQL database](https://ghtorrent.org/downloads.html) to compute every data set locally with our code.

### Directories
* **api** - Scripts for gathering stargazers and forkers of specific repositories via the GitHub API. Additional results of the bot detection and 100DaysOfCode participants search (both JSON)
* **data_verification** - Tools for comparing GHTorrent files with GitHub API data
* **gender_detector** - Location-based gender detection script for GitHub usernames using [gender-guesser](https://github.com/lead-ratings/gender-guesser) and [OSM](https://wiki.openstreetmap.org/wiki/API). Additional tools for computing country/continent distributions and converting gender-guesser regions to OSM country names
* **local** - Coding conventions, imports, observed events, color standards, Python CheatSheet 
* **misc** - Collection of scripts for simple numeric computations
* **plot** - Scripts for creating plots and plot data
* **repairCSV** - Tools for repairing corrupted GHTorrent csv files
* **saves** - Archive for relevant GitHub discussions (screenshots)
* **socialAnalysis** - Scripts for analysing comments on GitHub activities and the social follower network on the platform
* **statistical_tests** - Implementation of statistical tests like MWU, KS, chisquare, KL-divergence, RDD
* **streak_advanced** - Scripts for processing and analysing data from *streak_computation*. Technical details and explanations can be found in the thesis paper
* **streak_computation** - Scripts for filtering and computing the observed data using GHTorrent, including the computation of the streak database. A detailed description for every script can be found [here](https://github.com/lukasmoldon/GHStreaksThesis/blob/master/overview.xlsx). An overview for the streak computation is attached at the bottom of this page
* **tools** - Useful scripts used in the thesis (e.g. timezone converter)


### Streak computation and further analysis
The project starts, as described in the paper, with the computation of a streak database. The scripts can be found in the **streak_computation** folder. The streak database can be created with the following steps:

1. Download the latest [GHTorrent MySQL database](https://ghtorrent.org/downloads.html) and extract the files *commits.csv*, *project_commits.csv*, *projects.csv*, *users.csv*, *issues.csv*. Other files will be used in further analysis (e.g. **streak_advanced**), but are not required for creating the streak database.
2. Use *splitForkedProjects.py* to compute a list of non-forked project IDs (forks did not count for the streak feature), the script needs access to *projects.csv*.
3. Use the resulting list and *getStandaloneCommitIDs.py* to search for all related commit IDs of the non-forked projects, the script needs access to *project_commits.csv*.
4. Use the resulting list and *getCommitsPerUser.py* to count the number of commits in non-forked projects per user, the script needs access to *commits.csv*. This will be used to facilitate filtering for active users.
5. Use the counted commits per user and *reduceUsers.py* to filter out users with less than X commits in their lifetime on GitHub from the *users.csv*. The script creates a database of remaining users with personal information including the username, account creation date, status and location.
6. Filter the commit data from *commits.csv* with *reduceCommits.py*, as we only want the data of users in our new user subset and commits in non-forked projects (uses data from step 2 and 5).
7. Compute the size of the filtered user subset for each day with *getUsergroupsize.py*. This will be used for average value calculations in **streak_advanced**.
8. Filter the issue data from *issues.csv* with *reduceIssues.py* and with the same restrictions from step 6, as issues and pull-requests in/to non-forked projects also counted for the streak feature.  
9. Create a database including all types of contributions (commits, pull-requests, issues) assigned to the filtered subset of users with *getContributionPerUser.py*.
10. Create the final streak database using *getStreaks.py*. All contributions get sorted and transformed in the users local timezone, such that the resulting list contains streaks with a start and an end day for each user.

A graphical representation of the described process and the dependencies between the files can be found below, a detailed description of each script including output examples can be found in *overview.xlsx*. The computed files get analyzed under different aspects in the **streak_advanced** folder and can of course be used for further research.


### Overview for the streak computation
![Overview for streak_computation](https://github.com/lukasmoldon/GHStreaksThesis/blob/master/overviewGraphic.png)
