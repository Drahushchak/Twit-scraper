import tweepy as tw
import json
import os
import datetime

pathToProject = os.path.dirname(os.path.abspath(__file__))


class Twit_Scraper(object):
    def __init__(self):
        super().__init__()
        self.__config = self.__getJsonData('config.json')
        self.__init_credentials()
        self.__authenticate()

    def get_freq_dist(self, query, substring='', limit=0, case_sensitive=False):
        searched_tweets = tw.Cursor(self.api.search,
                                    q=query,
                                    tweet_mode='extended',
                                    ).items(limit)
        data = list()
        for tweet in searched_tweets:
            if not hasattr(tweet, 'retweeted_status'):
                data.append(tweet.full_text)
        words = [word if case_sensitive else word.lower()
                 for tweet in data 
                 for word in self.__word_tokenize(tweet)]

        result = {
            'tweets': len(data),
            'words': len(words),
            'freqDist': {
                word: words.count(word) 
                for word in set(words)
                if substring in word.lower()
            }
        }
        return result

    def __word_tokenize(self, string):
        temp = ''
        result = []
        whitelist_charecters = set(map(chr, range(ord('А'), ord('я') + 1)))
        whitelist_charecters.update(set('\'-ІЇЄҐіїєґ'))
        for c in string:
            if c in whitelist_charecters:
                temp += c
            elif temp:
                result.append(temp)
                temp = ''
        if temp:
            result.append(temp)
        return result

    def __authenticate(self):
        self.auth = tw.OAuthHandler(self.API_KEY, self.API_SECRET)
        self.auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)
        self.api = tw.API(self.auth)

    def __init_credentials(self):
        data = self.__getJsonData(self.__config['defaultCredentials'])
        self.API_KEY = data['consumer_key']
        self.API_SECRET = data['consumer_secret']
        self.ACCESS_TOKEN = data['access_token']
        self.ACCESS_TOKEN_SECRET = data['access_token_secret']

    def __getJsonData(self, file, inProjectData=True):
        path = os.path.abspath(
            f'{pathToProject}/Data/{file}') if inProjectData else os.path.abspath(file)
        with open(path, encoding='utf-8') as jsonFile:
            return json.load(jsonFile)


Twit_Scraper()
