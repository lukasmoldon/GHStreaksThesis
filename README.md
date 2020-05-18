# GHStreaksThesis
Code for my bachelor thesis on GitHub's streak feature (using data from GHTorrent). The thesis paper can be found [>>here<<](https://johanneswachs.com/papers/BachelorMoldon.pdf) .

## Directories
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




## Overview for the streak computation
![Overview for streak_computation](https://github.com/lukasmoldon/GHStreaksThesis/blob/master/overviewGraphic.png)

