import urllib
import json
import re
from datetime import datetime
import sys
import http
from pyquery import PyQuery


class TweetLib:
    base_url = 'https://twitter.com'
    max_tweets = 20
    username = ''
    since = ''
    until = ''
    query_search = ''
    top_tweets = ''


    def __init__(self, username='', max_tweets=20, since='', until='', \
                 query_search='', top_tweets=False):
        self.set_max_tweets(max_tweets)
        self.set_username(username)
        self.set_since(since)
        self.set_until(until)
        self.set_query_search(query_search)
        self.set_top_tweets(top_tweets)
        

    def set_username(self, username=''):
        """
        Set Twitter username to scrape
        
        Arguments:
            username {str} -- must be less then 16 chars, and alphanumeric + underscores
        """
        if username:
            if len(username) < 16 and re.match(r'[a-zA-Z_]\w+', username):
                self.username = username
            else:
                raise ValueError("Invalid Username")


    def set_since(self, since=''):
        """
        Set the date you want to start scraping tweets
        
        Arguments:
            since {str} -- date in the format YYYY-MM-DD
        """
        if since:
            r = re.compile('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')
            if len(since) == 10 and r.match(since) is not None:
                self.since = since
            else:
                raise ValueError("Invalid timestamp(YYYY-MM-DD): ", since)


    def set_until(self, until=''):
        """
        Set the date you want to stop scraping tweets
        
        Arguments:
            until {str} -- date in the format YYYY-MM-DD
        """
        if until:
            r = re.compile('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')
            if len(until) == 10 and r.match(until) is not None:
                self.until = until
            else:
                raise ValueError("Invalid timestamp(YYYY-MM-DD): ", until)


    def set_query_search(self, query_search=''):
        """
        Set a string to search on Twitter
        
        Arguments:
            query_search {str} -- query must be less then 280 chars
        """
        if query_search:
            if len(query_search) <= 280:
                self.query_search = query_search
            else:
                raise ValueError("Query String is too long(max_len:280)")


    def set_max_tweets(self, max_tweets=25):
        """
        Set max number of tweets to scrape
        
        Arguments:
            max_tweets {int} -- any positive integer
        """
        if str(max_tweets).isdigit() and max_tweets > 0:
            self.max_tweets = max_tweets
        else:
            raise ValueError("Invalid max_tweets(int): ", max_tweets)


    def set_top_tweets(self, top_tweets=False):
        """
        Return top tweets for a search/username
        
        Arguments:
            top_tweets {bool}
        """
        if type(top_tweets) == bool:
            self.top_tweets = top_tweets
        else:
            raise ValueError("Invalid top_tweets(bool): ", top_tweets)


    def get_tweets(self):
        """
        Scrape tweets, where all the magic starts 
        
        Returns:
            [list] -- list of scraped tweets
        """
        refresh_cursor = ''

        results = []
        cookie_jar = http.cookiejar.CookieJar()
        active = True

        while active:
            json = self.get_json_reponse(refresh_cursor, cookie_jar)
            if len(json['items_html'].strip()) == 0:
                break

            refresh_cursor = json['min_position']
            scraped_tweets = PyQuery(json['items_html'])

            # Remove incomplete tweets withheld by Twitter Guidelines
            scraped_tweets.remove('div.withheld-tweet')
            tweets = scraped_tweets('div.js-stream-tweet')

            if len(tweets) == 0:
                break

            for tweet_html in tweets:
                tweet_pq = PyQuery(tweet_html)
                
                tweet_username = tweet_pq("span.username b").text()
                # replace A tags with spaces
                formated_tweet = re.sub('<a[^<]+?>', ' ', tweet_pq("p.js-tweet-text").html())
                # remove all other HTML tags
                cleaned_tweet = re.sub('<[^<]+?>', '', formated_tweet)

                tweet = {
                    'id': tweet_pq.attr("data-tweet-id"),
                    'text': cleaned_tweet.strip(),
                    'username': tweet_username.split(' ')[0],
                    'retweets': int(tweet_pq(".ProfileTweet-action--retweet .ProfileTweet-actionCount").attr("data-tweet-stat-count")),
                    'favorites': int(tweet_pq(".ProfileTweet-action--favorite .ProfileTweet-actionCount").attr("data-tweet-stat-count")),
                    'replies': int(tweet_pq(".ProfileTweet-action--favorite .ProfileTweet-actionCount").attr("data-tweet-stat-count")),
                    'author_id': int(tweet_pq("a.js-user-profile-link").attr("data-user-id")),
                    'permalink': self.base_url + tweet_pq.attr("data-permalink-path"),
                    'mentions': re.compile('(@\\w*)').findall(cleaned_tweet),
                    'hashtags': re.compile('(#\\w*)').findall(cleaned_tweet),
                    'date': datetime.fromtimestamp(int(tweet_pq(".js-short-timestamp").attr("data-time")))
                }

                results.append(tweet)

                # break out when the max_tweet limit is hit
                if self.max_tweets > 0 and len(results) >= self.max_tweets:
                    active = False
                    break

        return results


    def get_json_reponse(self, refresh_cursor, cookie_jar):
        """
        Pull JSON file from Twitter and decode it
        
        Arguments:
            refresh_cursor -- tweet pagination
            cookie_jar -- page cookie
        
        Returns:
            [json] -- tweets in JSON format
        """
        url = self.create_url(refresh_cursor)

        headers = [
            ('Host', "twitter.com"),
            ('User-Agent', "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"),
            ('Accept', "application/json, text/javascript, */*; q=0.01"),
            ('Accept-Language', "de,en-US;q=0.7,en;q=0.3"),
            ('X-Requested-With', "XMLHttpRequest"),
            ('Referer', url),
            ('Connection', "keep-alive")
        ]

        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
        opener.addheaders = headers

        try:
            response = opener.open(url)
            json_response = response.read()
        except Exception as e:
            print(e)
            raise ValueError("Unexpected error:", sys.exc_info()[0])

        return json.loads(json_response.decode())
        

    def create_url(self, refresh_cursor):
        """
        Generate a Twitter valid URL to load JSON file from

        Arguments:
            refresh_cursor -- tweet pagination
            
        Returns:
            [str] -- formated URL string
        """
        url_data = ''
        if self.username:
            url_data += ' from:' + self.username

        if self.since:
            url_data += ' since:' + self.since

        if self.until:
            url_data += ' until:' + self.until

        if self.query_search:
            url_data += ' ' + self.query_search

        url = "/i/search/timeline?f=tweets&q=%s&src=typd&max_position=%s" % (urllib.parse.quote(url_data), refresh_cursor)
        return self.base_url + url
