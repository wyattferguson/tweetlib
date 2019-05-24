# Twitter Scraper
A python twitter scraper with no-api keys required. This is a refactoring and rewrite Jefferson Henrique's library [GetOldTweets-python](https://github.com/Jefferson-Henrique/GetOldTweets-python)

## Installation 
    pip3 install tweetlib


## How to use it 
All these parameters can be used in combination with one another. 

    ts = tweetlib.TweetLib(username="barackobama", max_tweets=10)

### Arguments

- username(str): any valid twitter name you want to scrape
- since("yyyy-mm-dd"): A lower bound date to restrict search.
- until("yyyy-mm-dd"):An upper bound date to restrict search.
- query_search(str): Search string
- top_tweets(bool): Return top tweets
- max_tweets(int): Max number of tweets you want to scrape.


## Examples

``` python
    from tweetlib import tweetlib
    # Get tweets by username
    ts = tweetlib.TweetLib(username="barackobama", max_tweets=10)
    tweets = ts.get_tweets()

    # Search for tweets
    ts = tweetlib.TweetLib(query_search="college", since="2018-01-01")
    tweets = ts.get_tweets()
```    


## Tweet Object
The tweet objects it returns in the list contain the following:

    tweet = {
        id (str)
        permalink (str)
        username (str)
        text (str)
        date (date)
        replies (int)
        retweets (int)
        favorites (int)
        mentions (str)
        hashtags (str)
    }



## Credit and Contact

Created by Wyatt Ferguson 

For any comments or questions your can reach me on Twitter [@wyattferguson](https://twitter.com/wyattferguson) or visit my little portfolio at [wyattf.dev](https://wyattf.dev)
