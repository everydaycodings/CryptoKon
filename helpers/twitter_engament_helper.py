import snscrape.modules.twitter as sntwitter
import pandas as pd
import numpy as np
import re
import plotly.express as px
import streamlit as st
from pandas.tseries.offsets import DateOffset
from datetime import datetime

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"  # flags (iOS)
                           "]+", flags=re.UNICODE)



def download_button(data, since, till, query, label="Download data as CSV"):

    button =st.download_button(
            label=label,
            data=data.to_csv(),
            file_name='{}-{}-{}_data.csv'.format(query, since, till),
            mime='text/csv',
            )
    
    return button


def cleanTxt(text):
    try:
        text = re.sub('@', '', text) #Removing @mentions
        text = re.sub('\$', '', text) #Removing $mentions
        text = re.sub('#', '', text) # Removing '#' hash tag
        text = re.sub('RT[\s]+', '', text) # Removing RT
        text = re.sub('https?:\/\/\S+', '', text)
        text = re.sub("\n","",text) # Removing hyperlink
        text = re.sub(":","",text) # Removing hyperlink
        text = re.sub("_","",text) # Removing hyperlink
        text = emoji_pattern.sub(r'', text)
    except:
        text = np.nan
    return text


@st.cache(allow_output_mutation=True)
def fetch_data(query_string, since_date, till_date, tweet_limit, save_data):
    
    query = "({}) until:{} since:{} -filter:replies".format(query_string, till_date, since_date)
    tweets = []
    limit = tweet_limit


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
    
    if save_data == True:
        df.to_csv("output/{}-{}-{}.csv".format(query, since_date, till_date)) 
    
    return df



def preprocess_data(data):

    data.dropna(inplace=True)

    data_types_dict = {'like_count': int, "followers_count": int, "retweet_count": int}
    data = data.astype(data_types_dict)

    data['Date'] = pd.to_datetime(data['Date'])
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')

    data["Tweet"] = data["Tweet"].apply(cleanTxt)

    return data


def default_twitter_engagement(data, twitter_query, since_date, until_date):

    number_of_twitter_engagement = data.groupby(["Date"]).size().reset_index(name="number of engagement")
    counter_chart = data.groupby(["Date"])[["like_count", "view_count", "followers_count", "retweet_count", "comments_count"]].mean().reset_index()
    total_engagement = number_of_twitter_engagement["number of engagement"].sum()

    st.text("Total Number Of Engagements: {}".format(total_engagement))

    fig = px.line(
    number_of_twitter_engagement,
    x="Date",
    y="number of engagement",
    )

    fig.add_bar(x=counter_chart["Date"], y=counter_chart["like_count"], name="Minimum Like Count")
    fig.add_bar(x=counter_chart["Date"], y=counter_chart["view_count"], name="Minimum View Count")
    fig.add_bar(x=counter_chart["Date"], y=counter_chart["retweet_count"], name="Minimum Retweet Count")
    fig.add_bar(x=counter_chart["Date"], y=counter_chart["comments_count"], name="Minimum Comments Count")

    fig.update_layout(title='Number Of Engagement For {} From:{} To:{}'.format(twitter_query, since_date, until_date),
                   xaxis_title='Date',
                   yaxis_title='Number Of Engagements')

    
    return st.plotly_chart(fig, theme="streamlit", use_container_width=True)



def like_view_count_engagement(data, x, y, x_title, y_title, title):

    counter_chart = data.groupby(["Date"])[["like_count", "view_count", "followers_count", "retweet_count", "comments_count"]].sum().reset_index()
    total_engagement = counter_chart[y].sum()

    fig = px.line(
    counter_chart,
    x=x,
    y=y,
    )


    fig.update_layout(title=title,
                   xaxis_title=x_title,
                   yaxis_title=y_title)

    return total_engagement, fig



def popular_user_engagement(data,condition, x_title, y_title, title):

    popular_user = data[(data['followers_count'] >= condition)]
    popular_user_of_twitter_engagement = popular_user.groupby(["Date"]).size().reset_index(name="number of engagement")
    counter_chart = popular_user.groupby(["Date"])[["like_count", "view_count", "followers_count", "retweet_count", "comments_count"]].min().reset_index()

    number_of_users = popular_user.shape[0]
    
    fig = px.line(
    popular_user_of_twitter_engagement,
    x="Date",
    y="number of engagement",
    )

    fig.add_bar(x=counter_chart["Date"], y=counter_chart["like_count"], name="Minimum Like Count")
    fig.add_bar(x=counter_chart["Date"], y=counter_chart["view_count"], name="Minimum View Count")
    fig.add_bar(x=counter_chart["Date"], y=counter_chart["retweet_count"], name="Minimum Retweet Count")
    fig.add_bar(x=counter_chart["Date"], y=counter_chart["comments_count"], name="Minimum Comments Count")

    fig.update_layout(title=title,
                   xaxis_title=x_title,
                   yaxis_title=y_title)

    return number_of_users, fig



def top_users(data):

    most_tweet_user = data.groupby(["User"]).size().sort_values(ascending=False).reset_index(name="Number of times Occured")
    top_user_list = most_tweet_user.head()

    most_followed_user = data.sort_values('followers_count', ascending=False).drop_duplicates(subset=["User"])
    most_followed_user = data[["User", "followers_count", "Date"]].rename(columns={"followers_count": "Number Of Followers", "Date": "Last Updated"}).sort_values("Number Of Followers", ascending=False).reset_index().head()

    return top_user_list, most_followed_user



def unique_user_engagement(data):

    unique_user = data.groupby(['Date'])['User'].nunique().reset_index().rename(columns={"User": "Number Of Unique Users"})

    fig = px.line(
    unique_user,
    x="Date",
    y="Number Of Unique Users",
    )

    fig.update_layout(title="Number Of Unique Users Twitting Everyday",
                   xaxis_title="Date",
                   yaxis_title="Number Of Unique Users")

    return fig


def engagement_percentage_change(data):

    transformed_data = data.sort_values(by=["Date"], ascending=True)
    transformed_data = transformed_data.groupby(["Date"]).size().reset_index(name="number")
    from_time = transformed_data.head(1)["number"].values[0]

    end_time = transformed_data.tail(1)["number"].values[0]

    try:
        all_time_change = "{}%".format('%.2f' %float(((end_time - from_time)/from_time) *100))
    except:
        all_time_change = "No Data"

    try:
        six_months_interval = (datetime.strptime(transformed_data.tail(1)["Date"].values[0], '%Y-%m-%d')  - DateOffset(months=6)).strftime("%Y-%m-%d")
        six_months_from_time = transformed_data.loc[transformed_data["Date"] == six_months_interval].head(1)["number"].values[0]
        six_month_time_change = "{}%".format('%.2f' %float(((end_time - six_months_from_time)/six_months_from_time) *100))
    except:
        six_month_time_change = "No Data"

    try:
        one_month_interval = (datetime.strptime(transformed_data.tail(1)["Date"].values[0], '%Y-%m-%d')  - DateOffset(months=1)).strftime("%Y-%m-%d")
        one_month_from_time = transformed_data.loc[transformed_data["Date"] == one_month_interval].head(1)["number"].values[0]
        one_month_time_change = "{}%".format('%.2f' %float(((end_time - one_month_from_time)/one_month_from_time) *100))
    except:
        one_month_time_change = "No Data"
    
    try:
        one_week_interval = (datetime.strptime(transformed_data.tail(1)["Date"].values[0], '%Y-%m-%d')  - DateOffset(weeks=1)).strftime("%Y-%m-%d")
        one_week_from_time = transformed_data.loc[transformed_data["Date"] == one_week_interval].head(1)["number"].values[0]
        one_week_time_change = "{}%".format('%.2f' %float(((end_time - one_week_from_time)/one_week_from_time) *100))
    except:
        one_week_time_change = "No Data"

    try:
        one_day_interval = (datetime.strptime(transformed_data.tail(1)["Date"].values[0], '%Y-%m-%d')  - DateOffset(days=1)).strftime("%Y-%m-%d")
        one_day_from_time = transformed_data.loc[transformed_data["Date"] == one_day_interval].head(1)["number"].values[0]
        one_day_time_change = "{}%".format('%.2f' %float(((end_time - one_day_from_time)/one_day_from_time) *100))
    except:
        one_day_time_change = "No Data"

    return all_time_change, six_month_time_change, one_month_time_change, one_week_time_change, one_day_time_change
    

def counter_percentage_change(data, column_name):

    transformed_data = data.sort_values(by=["Date"], ascending=True)
    transformed_data = transformed_data.groupby(["Date"])[["like_count", "view_count", "followers_count", "retweet_count", "comments_count"]].sum().reset_index()
    from_time = transformed_data.head(1)[column_name].values[0]

    end_time = transformed_data.tail(1)[column_name].values[0]

    try:
        all_time_change = "{}%".format('%.2f' %float(((end_time - from_time)/from_time) *100))
    except:
        all_time_change = "No Data"

    try:
        six_months_interval = (datetime.strptime(transformed_data.tail(1)["Date"].values[0], '%Y-%m-%d')  - DateOffset(months=6)).strftime("%Y-%m-%d")
        six_months_from_time = transformed_data.loc[transformed_data["Date"] == six_months_interval].head(1)[column_name].values[0]
        six_month_time_change = "{}%".format('%.2f' %float(((end_time - six_months_from_time)/six_months_from_time) *100))
    except:
        six_month_time_change = "No Data"

    try:
        one_month_interval = (datetime.strptime(transformed_data.tail(1)["Date"].values[0], '%Y-%m-%d')  - DateOffset(months=1)).strftime("%Y-%m-%d")
        one_month_from_time = transformed_data.loc[transformed_data["Date"] == one_month_interval].head(1)[column_name].values[0]
        one_month_time_change = "{}%".format('%.2f' %float(((end_time - one_month_from_time)/one_month_from_time) *100))
    except:
        one_month_time_change = "No Data"
    
    try:
        one_week_interval = (datetime.strptime(transformed_data.tail(1)["Date"].values[0], '%Y-%m-%d')  - DateOffset(weeks=1)).strftime("%Y-%m-%d")
        one_week_from_time = transformed_data.loc[transformed_data["Date"] == one_week_interval].head(1)[column_name].values[0]
        one_week_time_change = "{}%".format('%.2f' %float(((end_time - one_week_from_time)/one_week_from_time) *100))
    except:
        one_week_time_change = "No Data"

    try:
        one_day_interval = (datetime.strptime(transformed_data.tail(1)["Date"].values[0], '%Y-%m-%d')  - DateOffset(days=1)).strftime("%Y-%m-%d")
        one_day_from_time = transformed_data.loc[transformed_data["Date"] == one_day_interval].head(1)[column_name].values[0]
        one_day_time_change = "{}%".format('%.2f' %float(((end_time - one_day_from_time)/one_day_from_time) *100))
    except:
        one_day_time_change = "No Data"


    return all_time_change, six_month_time_change, one_month_time_change, one_week_time_change, one_day_time_change


def moving_average_engagement(data):
    
    number_of_twitter_engagement = data.groupby(["Date"]).size().reset_index(name="number of engagement")
    number_of_twitter_engagement['7_day_moving_average'] = number_of_twitter_engagement['number of engagement'].rolling(7).mean()
    number_of_twitter_engagement['14_day_moving_average'] = number_of_twitter_engagement['number of engagement'].rolling(14).mean()
    number_of_twitter_engagement['30_day_moving_average'] = number_of_twitter_engagement['number of engagement'].rolling(30).mean()
    number_of_twitter_engagement['60_day_moving_average'] = number_of_twitter_engagement['number of engagement'].rolling(60).mean()
    pd.options.plotting.backend = "plotly"
    fig_plot = number_of_twitter_engagement.plot(x='Date', y=['number of engagement', "7_day_moving_average", "14_day_moving_average", "30_day_moving_average", "60_day_moving_average"])
    
    return fig_plot


def moving_average_like_view_count(data, y):

    counter_chart = data.groupby(["Date"])[["like_count", "view_count", "followers_count", "retweet_count", "comments_count"]].sum().reset_index()
    
    counter_chart['7_day_moving_average'] = counter_chart[y].rolling(7).mean()
    counter_chart['14_day_moving_average'] = counter_chart[y].rolling(14).mean()
    counter_chart['30_day_moving_average'] = counter_chart[y].rolling(30).mean()
    counter_chart['60_day_moving_average'] = counter_chart[y].rolling(60).mean()
    pd.options.plotting.backend = "plotly"
    fig_plot = counter_chart.plot(x='Date', y=[y, "7_day_moving_average", "14_day_moving_average", "30_day_moving_average", "60_day_moving_average"])

    return fig_plot