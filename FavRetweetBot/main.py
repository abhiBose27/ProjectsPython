import tweepy
import config
import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)


def create_api():
    auth = tweepy.OAuthHandler(config.API_KEY, config.API_KEY_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api


def get_last_tweet_id(file):
    try:
        f = open(file, 'r')
        lastId = int(f.read().strip())
        f.close()
    except:
        lastId = 0
    return lastId


def write_last_tweet_id(file, Id):
    f = open(file, 'w')
    f.write(str(Id))
    f.close()
    logger.info("Updated the file with the latest tweet ID")


def main(file='tweet_id.txt'):
    api = create_api()
    last_id = get_last_tweet_id(file)
    if last_id != 0:
        tweets = api.user_timeline(screen_name="premierleague", since_id=last_id, count=100, include_rts=False)
    else:
        tweets = api.user_timeline(screen_name="premierleague", count=100, include_rts=False)
    new_id = 0
    if len(tweets) == 0:
        return
    for tweet in tweets:
        new_id = tweet.id
        if "Arsenal" in tweet.text:
            if tweet.in_reply_to_status_id is not None:
                return
            if not tweet.favorited:
                tweet.favorite()
                logger.info("liking the tweet")
            else:
                logger.info("already liked to {}".format(tweet.id))
            if not tweet.retweeted:
                tweet.retweet()
                logger.info("retweeting the tweet")
            else:
                logger.info("already retweeted to {}".format(tweet.id))

    write_last_tweet_id(file, new_id)


if __name__ == "__main__":
    main()
