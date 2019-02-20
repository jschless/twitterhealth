# Twitter Health


## Goal
We are creating a classifier for tweets to help users determine the credibility / reliability of a tweet. Ultimately, we will be able to classify tweets based on their text, associated users, and the associated tweet network. Using Twitter's streaming API, we will produce a GUI that allows a user to interact with Twitter while being warned of the potential dangers.


## Dataset
We use the PHEME dataset in this project. The dataset can be found here: [PHEME](https://figshare.com/articles/PHEME_rumour_scheme_dataset_journalism_use_case/2068650)

## Files
- tweet.py : This file defines the Tweet and User data structure along with some useful functions
- phemeParser.py : This file processes the PHEME dataset into a list of annotated conversation threads
- classifier.py : This file trains a classifier on the PHEME dataset according to features
- features.py : This file contains all of the feature engineering
- tester.py : This file supports classifying new datasets according to our classifier
- credBankParser.py : This file supports parsing the credBank dataset to bolster our training data
- electionInterferenceParser.py : This file supports parsing recent election interference data released by twitter. This provides a formidable test set for our classifier.

## Folders
- Datasets: contains information on the datasets of this project as well as some small sets, like the Iranian fake news tweets

- Scratchwork: This folder contains some scratch work.
## Contributors
- Pat Cowley
- Grayson Osborne
- Joe Schlessinger
- Matthew Yuan
