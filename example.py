import tweetscraper

ts = tweetscraper.TweetScraper(username="jon_bois", max_tweets=2)

tweets = ts.get_tweets()
for t in tweets:
    print(t)