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
- twitterhealth.py : This is the main file for running the project code

## How to Run Our Code
It is easy to get this code working and reproduce our results.

# Setting up the Development Environment
1. You will need Python 3. Download the PHEME dataset found here: [PHEME](https://figshare.com/articles/PHEME_rumour_scheme_dataset_journalism_use_case/2068650).

2. Create a config file called `twitconfig.py` with the access keys from your Twitter application. The contents of the code should be as follows but replacing the values in the dictionary with your individual account values. Add the path to the pheme dataset in this config file.
~~~~
twitter = {'consumer_key': 'L6JvqYzvUeHX36sYTR8O3E7gD',
            'consumer_secret': 'VKVPjkonSRUBzOsaiNKdcFToDISJ0ga3vGGvNuDo6nAfRtABU1',
            'access_token': '1052184206368002049-9RSvx4QK9Js4gnMrMY8GCMvQYYPtPJ',
            'access_token_secret': 'KUykgZdc8vIzDph3CasS91i7foWks8Y6NtLTpBxPTl3BR'
}
pheme_path = 'C:\\Users\\EECS\\Documents'
~~~~

3. Install python packages as necessary.

# Running the code
All scripts are run through twitterhealth.py. At the command line, simply run 'twitterhealth.py'. You will be given instructions on how to run it:
~~~~
twitterhealth.py [-c -t -v]
-c or classifier : only runs classifier
-t or twitter : runs classifier within twitter GUI
-v or verbose : prints extra information
~~~~

- -c is meant for running the classifier on only the training data set
- -v prints more detailed information about the classifier's performance
- -t opens our Twitter GUI and applies the classifier to each tweet

# Adding Features
One of the advantages of our code design is easy addition of features. Simply add the feature to features.py. (It must take a tweet object from tweet.py as an argument). Below is an example of a simple feature that computes following ratio:

~~~~
def follow_ratio(tweet):
    user = tweet.user
    if user.friends_count == 0:
        print(user)
        return 0
    return (user.followers_count/user.friends_count)
~~~~

Next, you add it to the input vector. Within classification.py, edit the function buildInput().

~~~~
inputs = pd.DataFrame()
inputs['follow_ratio'] = data.apply(follow_ratio)
inputs['graph_follow_ratio'] = data.apply(
      lambda x : graph_weight(x, follow_ratio)
)
inputs['sentiment'] = data.apply(sentiment)
return inputs
~~~~~

The formula for adding is simply `inputs['name_of_feature'] = data.apply(name_of_function) ` Here, it will be used in both the training of the model and the Twitter GUI.

## Contributors
- Pat Cowley
- Grayson Osborne
- Joe Schlessinger
- Matthew Yuan
