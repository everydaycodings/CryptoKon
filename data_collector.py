import snscrape.modules.twitter as sntwitter
import pandas as pd



def fetch_data():

    query = input("Enter Your Query: ")
    since  = input("Enter your date since you want to collect data(yy-mm-dd): ")
    until  = input("Enter your date until you want to collect data(yy-mm-dd): ")
    limit = input("Enter the limit of your tweets you want to collect: ")
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



fetch_data()