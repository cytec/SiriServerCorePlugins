#!/usr/bin/python
# -*- coding: utf-8 -*-

#author: cytec iamcytec@googlemail.com
#todo: da ist noch viel möglich
#project: SiriServer
#commands:
#   twitter sende !Nachricht!
#   twitter updates
#easy_install python-twitter

from plugin import *
import oauth2
import twitter
import re

cs_key = APIKeyForAPI("twitter_consumer_key")
cs_secret = APIKeyForAPI("twitter_consumer_secret")
ac_key = APIKeyForAPI("twitter_access_token_key")
ac_secret = APIKeyForAPI("twitter_access_token_secret")
twitterUser = APIKeyForAPI("twitter_username")

res = {
    'setTweet': {
        'de-DE': 'twitter sende (.*)',
        'en-US': 'tweet (.*)'
    },
    'reallyTweet': {
        'de-DE': 'Soll ich dein Tweet senden?: ',
        'en-US': 'Should i post your Tweet?: '
    },
    'tweeted': {
        'de-DE': 'Tweet gesendet: ',
        'en-US': 'tweet sended: '
    },
    'cancel': {
        'de-DE': 'Ok, du bist der Boss',
        'en-US': 'OK, your the boss'
    },
    'getUpdates': {
        'de-DE': 'twitter (updates|neues|neuigkeiten|news)',
        'en-US': 'twitter (updates|news|latest news)'
    },
    'fetchingUpdates': {
        'de-DE': 'Hier sind die 5 neusten tweets',
        'en-US': 'here are the 5 latest tweets'
    }
}

helpPhrases = {
    'en-US': u'tweet, twitter updates, twitter news',
    'de-DE': u'twitter sende, twitter updates, twitter news',
}

class tweet(Plugin):

    @register("de-DE", res['setTweet']['de-DE'])
    @register("en-US", res['setTweet']['en-US'])
    def tweet_status(self, speech, language):
        tapi = twitter.Api(consumer_key=cs_key, consumer_secret=cs_secret, access_token_key=ac_key, access_token_secret=ac_secret)
        TweetString = re.match(res['setTweet'][language], speech, re.IGNORECASE)
        answer = self.ask(res['reallyTweet'][language] + TweetString.group(1))    
        if answer.lower() == 'ja' or answer.lower() == 'yes' or answer.lower() == 'yeah' or answer.lower() == 'jup<':
            tweetstatus = tapi.PostUpdate(TweetString.group(1))
            self.say(res['tweeted'][language] + TweetString.group(1))
        else:
            self.say(res['cancel'][language]) 
        self.complete_request()

    @register('de-DE', res['getUpdates']['de-DE'])
    @register('en-US', res['getUpdates']['en-US'])
    def twitter_updates(self, speech, language):
        tapi = twitter.Api(consumer_key=cs_key, consumer_secret=cs_secret, access_token_key=ac_key, access_token_secret=ac_secret)
        updates = tapi.GetFriendsTimeline(count=5)
        self.say(res['fetchingUpdates'][language])
        for message in updates:
            name = message.user.name
            text = message.text
            answer = name + ": " + text
            self.say(answer, ' ')
        self.complete_request()