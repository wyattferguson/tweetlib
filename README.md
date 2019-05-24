# Twitter Scraper
A python twitter scraper with no-api keys required. This is a refactoring and rewrite Jefferson Henrique's library [GetOldTweets-python](https://github.com/Jefferson-Henrique/GetOldTweets-python)

## Installation 
    pip3 install tweetlib


## How to use it 
All these parameters can be used in combination with one another. Alternatively you can pass the variables in when you create an new instance of the library.

    ts = tweetlib.TweetLib(username="barackobama", max_tweets=10)

### Arguments

- username(str): any valid twitter name you want to scrape
- since("yyyy-mm-dd"): A lower bound date to restrict search.
- until("yyyy-mm-dd"):An upper bound date to restrict search.
- query_search(str): Search string
- top_tweets(bool): Return top tweets
- max_tweets(int): Max number of tweets you want to scrape.


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


## Examples

``` python
    from tweetlib import tweetlib
    # Get tweets by username
    ts = tweetlib.TweetLib(username="barackobama")
    tweets = ts.get_tweets()

    # or you can use the set method instead
    ts = tweetlib.TweetLib()
    ts.set_username("barackobama")
    tweets = ts.get_tweets()

    # Search for tweets
    ts = tweetlib.TweetLib()
    ts.set_query_search("college")
    ts.set_max_tweets(100)
    tweets = ts.get_tweets()
```    


## Credit and Contact

Created by Wyatt Ferguson 

For any comments or questions your can reach me on Twitter [@wyattferguson](https://twitter.com/wyattferguson) or visit my little portfolio at [wyattf.dev](https://wyattf.dev)
