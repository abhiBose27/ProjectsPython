import time
import datetime
import os
import csv
import tweepy
import config
import sys


# To check if the tweet is in English language
def isEnglish(text):
    try:
        text.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def getWoeid(api, locations):
    all_trends = api.available_trends()
    places = {loc['name'].lower(): loc['woeid'] for loc in all_trends}
    woeids = []
    for location in locations:
        if location in places:
            woeids.append(places[location])
        else:
            print("ERR: ", location, " woeid does not exist in trending topics")
    return woeids


# Authentication of keys and get the API
def create_api():
    auth = tweepy.OAuthHandler(config.API_KEY, config.API_KEY_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api


# Get the trending hashtags of the given locations
def trending_hashTags(api, location):
    woeids = getWoeid(api, location)
    trending = set()
    for woeid in woeids:
        try:
            trends = api.get_place_trends(woeid)
        except:
            print("API limit exceeded")
            time.sleep(3605)
            trends = api.get_place_trends(woeid)
        topics = [trend['name'][1:] for trend in trends[0]['trends'] if (trend['name'].find('#') == 0 and
                                                                         isEnglish(trend['name']))]
        trending.update(topics)
    return trending


# Get the popular tweets of those hashtags
def get_tweets(api, hashTags):
    tweets = []
    for tweet in tweepy.Cursor(api.search_tweets,
                               q=hashTags,
                               count=1000,
                               result_type='popular',
                               include_entities=True,
                               lang="en").items():
        if isEnglish(tweet.text):
            tweets.append([tweet.id_str, hashTags, tweet.created_at.strftime('%d-%m-%Y %H:%M'), tweet.user.screen_name,
                           tweet.text])
    return tweets


# Create the csv file of hashtags and tweets from those hashtags
def twitter_bot(api, locations):
    today = datetime.datetime.today().strftime("%d-%m-%Y")
    if not os.path.exists("trending_tweets"):
        os.makedirs("trending_tweets")
    file_tweets = open("trending_tweets\\" + today + "-tweets.csv", "a+")
    file_hashtags = open("trending_tweets\\" + today + "-hashtags.csv", "w+")
    writer = csv.writer(file_tweets)

    hashtags = trending_hashTags(api, locations)
    file_hashtags.write("\n".join(hashtags))
    print("Hashtags written to file.")
    file_hashtags.close()

    for hashtag in hashtags:
        try:
            print("Getting Tweets for the hashtag: ", hashtag)
            tweets = get_tweets(api, "#" + hashtag)
        except:
            print("API limit exceeded. Waiting for next hour")
            time.sleep(3605)  # change to 0.2 sec for testing
            tweets = get_tweets(api, "#" + hashtag)
        for tweet in tweets:
            writer.writerow(tweet)

    file_tweets.close()


def main():
    locations = sys.argv
    locations.pop(0)
    api = create_api()
    twitter_bot(api, locations)


if __name__ == "__main__":
    main()
