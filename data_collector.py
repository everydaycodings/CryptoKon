import snscrape.modules.twitter as sntwitter
import pandas as pd
from helpers.twitter_ai_helper import add_sentiment_score_labels, getPolarity, get_sentiment_polarity



def fetch_data():

    query = input("Enter Your Query: ")
    since  = input("Enter your date since you want to collect data(yy-mm-dd): ")
    until  = input("Enter your date until you want to collect data(yy-mm-dd): ")
    limit = input("Enter the limit of your tweets you want to collect: ")
    sentiment = input("Do you want to analyze sentiment of the tweets?(y/n): ")
    query = "({}) until:{} since:{} -filter:replies".format(query, until, since)
    tweets = []

    print("Started Collecting Tweets...")
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        
        #print(vars(tweet))
        #break
        if len(tweets) == limit:
            break
        else:
            if tweet.viewCount == None or tweet.mentionedUsers == None:

                if tweet.viewCount == None:
                    viewCount = 0
                    try:
                        tweets.append([tweet.date, tweet.user.username, tweet.rawContent, tweet.url, tweet.likeCount, tweet.user.followersCount, tweet.retweetCount, tweet.user.verified, viewCount, len(tweet.mentionedUsers), tweet.quoteCount])
                    except:
                        tweets.append([tweet.date, tweet.user.username, tweet.rawContent, tweet.url, tweet.likeCount, tweet.user.followersCount, tweet.retweetCount, tweet.user.verified, viewCount, 0, tweet.quoteCount])
                
                elif tweet.mentionedUsers == None:
                    mentioneduser = 0
                    tweets.append([tweet.date, tweet.user.username, tweet.rawContent, tweet.url, tweet.likeCount, tweet.user.followersCount, tweet.retweetCount, tweet.user.verified, tweet.viewCount, mentioneduser, tweet.quoteCount])
            else:
                tweets.append([tweet.date, tweet.user.username, tweet.rawContent, tweet.url, tweet.likeCount, tweet.user.followersCount, tweet.retweetCount, tweet.user.verified, tweet.viewCount, len(tweet.mentionedUsers), tweet.quoteCount])
         
    df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet', "url", "like_count", "followers_count", "retweet_count", "verified", "view_count", "mentionuser", "comments_count"])

    df.to_csv('output/{}-{}-{}.csv'.format(query, since, until))

    print("Tweets Collection Completed")
    print("tweets data has been saved.")

    if sentiment == "y" or "Y" or "YES" or "yes":
        print("Started Analyzing the sentiment")
        df = add_sentiment_score_labels(df)
        print("Sentiment Analization Completed")
        df.to_csv('output/{}-{}-{}.csv'.format(query, since, until))
        print("Data has been saved")
        print("Started Analyzing the polarity")
        df = get_sentiment_polarity(data=df)
        df.to_csv('output/{}-{}-{}.csv'.format(query, since, until))
        print("Polarity Analization Completed")
        print("Data has been saved")



fetch_data()