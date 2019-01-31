from tweet import *

def follow_ratio(user):
    return (user.follower_count/user.following_count)

def sentiment(tweet):
    import requests
    url = 'http://text-processing.com/api/sentiment'
    input = tweet.tweet_text
    payload = {'text' : input}
    print(payload)
    r = requests.post(url,data=payload)
    print(r)
    output = r.json()
    pos = output['probability']['pos']
    neg = output['probability']['neg']
    neutral = output['probability']['neutral']
    return pos
