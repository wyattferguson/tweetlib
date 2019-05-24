import twttrscrape

ts = twttrscrape.TwitterScraper(username="wyattferguson", max_tweets=10)
tweets = ts.get_tweets()
for t in tweets:
    print(t)
    

ts = twttrscrape.TwitterScraper(query_search="college")
ts.set_max_tweets(25)
tweets = ts.get_tweets()
for t in tweets:
    print(t)
    