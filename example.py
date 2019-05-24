from tweetlib import tweetlib

ts = tweetlib.TweetLib(username="wyattferguson", max_tweets=10)
tweets = ts.get_tweets()
for t in tweets:
    print(t)
