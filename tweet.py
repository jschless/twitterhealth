class Tweet:
    def __init__(self, text, favCount, retCount, id, isReply, user):
        self.tweet_text=text
        self.favorite_count = favCount
        self.retweet_count = retCount
        self.user = user
        self.tweetid = id
        self.is_reply = isReply
        self.reply_list = None
        self.annotation = None

    def __init__(self, dataframe):
        self.tweetid = dataframe['tweetid']
        self.userid = dataframe['userid']
        self.user = User(dataframe)
        self.tweet_language = dataframe['tweet_language']
        self.tweet_text = dataframe['tweet_text']
        self.tweet_time = dataframe['tweet_time']
        self.in_reply_to_userid = dataframe['in_reply_to_userid']
        self.in_reply_to_tweetid = dataframe['in_reply_to_tweetid']
        self.quoted_tweet_tweetid = dataframe['quoted_tweet_tweetid']
        self.is_retweet = dataframe['is_retweet']
        self.retweet_userid = dataframe['retweet_userid']
        self.retweet_tweetid = dataframe['retweet_tweetid']
        self.latitude = dataframe['latitude']
        self.longitude = dataframe['longitude']
        self.quote_count = dataframe['quote_count']
        self.reply_count = dataframe['reply_count']
        self.favorite_count = dataframe['like_count']
        self.retweet_count = dataframe['retweet_count']
        self.hashtags = dataframe['hashtags']
        self.urls = dataframe['urls']
        self.user_mentions = dataframe['user_mentions']

    def __str__(self):
        return self.tweet_text + ' - ' + self.user.name

    def to_dict(self):
        return {
            'tweet_text' : self.tweet_text,
            'favorite_count' : self.favorite_count,
            'ret_count' : self.retCount,
            'user' : self.user,
            'tweetid' : self.id,
            'reply' : self.isReply,
            'annotation' : self.annotation,
            'replyList' : self.replyList
        }

class User:
    def __init__(self, name, screenName, favorite_count, follower_count, description, verified, friends_count):
        self.display_name = name
        self.screen_name = screenName
        self.favorite_count = favorite_count
        self.follower_count = follower_count
        self.description = description
        self.verified = verified
        self.friends_count = friends_count

    def __init__(self, dataframe):
        self.userid= dataframe['userid']
        self.display_name = dataframe['user_display_name']
        self.screen_name = dataframe['user_screen_name']
        self.user_reported_location = dataframe['user_reported_location']
        self.user_profile_description = dataframe['user_profile_description']
        self.user_profile_url = dataframe['user_profile_url']
        self.follower_count = dataframe['follower_count']
        self.following_count = dataframe['following_count']
        self.account_creation_date = dataframe['account_creation_date']
        self.account_language = dataframe['account_language']

def processDataSet(path):
    tweets = {}
    users = {}
    df = pd.read_csv(path)
    for row in range(len(df)):
        tweet = Tweet(df.iloc[row])
        tweets[tweet.tweetid] = tweet
        users[tweet.userid] = tweet.user

    for tweetid, tweet in tweets.items():
        print(str(tweet))
