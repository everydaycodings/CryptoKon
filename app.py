import streamlit as st
import plotly.express as px
from helpers.token_details_helper import get_asset_list, get_asset_id, asset_overview, crypto_desc, asset_details_v2, ico_details
from helpers.token_details_helper import token_statics, fetch_token_allocation, update_list
from helpers.twitter_engament_helper import fetch_data, preprocess_data
from helpers.twitter_engament_helper import default_twitter_engagement, like_view_count_engagement, popular_user_engagement, top_users, unique_user_engagement, engagement_percentage_change, counter_percentage_change
from helpers.twitter_engament_helper import download_button, moving_average_engagement, moving_average_like_view_count
from helpers.twitter_ai_helper import plot_sentiment_pie, plot_sentiment_confidence_line, plot_sentiment_score_line
import plotly.express as px
import pandas as pd



st.set_page_config(
     page_title="Crypto Twitter Analysis Web App",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://github.com/everydaycodings',
         'About': "### APP Version: v1.1.1\nCryptoKon is a revolutionary web application that helps you stay ahead of the curve in the ever-changing world of cryptocurrency. With its advanced analysis tools, CryptoKon provides a deep understanding of the trends and movements within specific crypto projects, empowering you to make informed investment decisions. Say goodbye to sifting through endless data and hello to a streamlined, user-friendly platform that puts the power of crypto analysis at your fingertips.\n #### Developer: [everydaycodings](https://github.com/everydaycodings)\n #### Connect with me: [https://linktr.ee/everydaycodings](https://linktr.ee/everydaycodings)"
     }
)


st.title("Crypto Data Analysis")
st.write("Sample of a CSV file")
st.dataframe(pd.read_csv("files/sample.csv", engine='python').head())
sample_data = pd.read_csv("files/full_sample.csv", engine='python')
download_button(data=sample_data, since="sample", till="data", query="cryptokon", label="Download Sample Data")



uploaded_file = st.file_uploader("If You an csv file already then upload it (Optional)",type="csv", help="You have to upload the csv file in the same format as it is seen above example.")
twitter_query = st.text_input("Enter the text you want to search in Twitter")
with st.expander("Dont Know what to search? See this:"):
    st.markdown("```$ADA``` => To search all the Tweets which contains $ADA Word.")
    st.markdown("```#ADA``` => To search all the Tweets which contains #ADA Word.")
    st.markdown("```$ADA OR #ADA``` => To search all the Tweets which contains #ADA or #ADA Word.")
    st.markdown("```from:saksham``` => To search all the Tweets from the username saksham.")
    st.markdown("```#github (from:everydaycodings)``` => To search all the Tweets from the username saksham which contains word #github.")
since_date = st.date_input("Enter the date you want to collect date From: ")
until_date = st.date_input("Enter the date you want to collect data To: ")
number_of_tweets = st.slider("How many tweets You want to collect from {} Limit: 1K to 10M".format(twitter_query), min_value=1000, max_value=10000000, step=1, value=1000000)
save_data = st.selectbox("Do You want to save the Twitter data: ", options=[False, True])
sentiment_analysis = st.selectbox("Do You want to analyze the Twitter Sentiment: ", options=[False, True])
crypto_choice = st.selectbox("Select your crypto", options=get_asset_list())
st.text("If You have not got your crypto in the above list try Updating the List.")
if st.button("Update The List"):
    update_list()
    st.success("List Updated")
st.info("If You are fetching data for long timeframe and if your seach query is popular it may take long time, so i request you to be patient.")




if st.button("Show Data"):

    st.title(" ")
    st.title("Your Results Are Here")

    if uploaded_file:
        data = pd.read_csv(uploaded_file, engine='python')
    else:
        data = fetch_data(query_string=twitter_query, since_date=since_date, till_date=until_date, tweet_limit=number_of_tweets, save_data=save_data, sentiment_analysis=sentiment_analysis)
    data = preprocess_data(data)
    
    st.dataframe(data)
    download_button(data=data, since=since_date, till=until_date, query=twitter_query)


    default_twitter_engagement(data=data, twitter_query=twitter_query, since_date=since_date, until_date=until_date)

    
    number_counts1, fig1 = like_view_count_engagement(data=data, x="Date", y="like_count", x_title="Date", y_title="Number Of Likes", title="Total Number of likes per day")
    number_counts2, fig2 = like_view_count_engagement(data=data, x="Date", y="view_count", x_title="Date", y_title="Number Of Views", title="Total Number of Views per day")
    number_counts3, fig3 = like_view_count_engagement(data=data, x="Date", y="retweet_count", x_title="Date", y_title="Number Of Retweets", title="Total Number of Reweets per day")
    number_counts4, fig4 = like_view_count_engagement(data=data, x="Date", y="comments_count", x_title="Date", y_title="Number Of Comments", title="Total Number of Comments per day")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Likes Engagement", "Views Engagement", "Retweets Engagement", "Comments Engagement"])
    with tab1:
        st.text("Total Number Of Likes: {}".format(number_counts1))
        st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
    with tab2:
        st.text("Total Number Of Views: {}".format(number_counts2))
        st.plotly_chart(fig2, theme="streamlit", use_container_width=True)
    with tab3:
        st.text("Total Number Of Retweets: {}".format(number_counts3))
        st.plotly_chart(fig3, theme="streamlit", use_container_width=True)
    with tab4:
        st.text("Total Number Of Comments: {}".format(number_counts4))
        st.plotly_chart(fig4, theme="streamlit", use_container_width=True)


    users_count1, user_popular_fig1 = popular_user_engagement(data=data, condition=10000, x_title="Date", y_title="Number Of Engagements", title="Number of Engagements an account with 10k Followers")
    users_count2, user_popular_fig2 = popular_user_engagement(data=data, condition=100000, x_title="Date", y_title="Number Of Engagements", title="Number of Engagements an account with 100k Followers")
    users_count3, user_popular_fig3 = popular_user_engagement(data=data, condition=500000, x_title="Date", y_title="Number Of  Engagements", title="Number of Engagements an account with 500k Followers")
    
    tab4, tab5, tab6 = st.tabs(["10k Account", "100k Account", "500k Account"])
    with tab4:
        st.text("Number Of users: {}".format(users_count1))
        st.plotly_chart(user_popular_fig1, theme="streamlit", use_container_width=True)
    with tab5:
        st.text("Number Of users: {}".format(users_count2))
        st.plotly_chart(user_popular_fig2, theme="streamlit", use_container_width=True)
    with tab6:
        st.text("Number Of users: {}".format(users_count3))
        st.plotly_chart(user_popular_fig3, theme="streamlit", use_container_width=True)


    st.plotly_chart(unique_user_engagement(data=data), theme="streamlit", use_container_width=True)


    st.subheader("Moving Averages for Tweets Engagements")
    st.plotly_chart(moving_average_engagement(data),  theme="streamlit", use_container_width=True)


    st.subheader("Moving Averages for Likes, Views, Retweets and Comments Engagements")
    tab7, tab8, tab9, tab10 = st.tabs(["Likes Engagement", "Views Engagement", "Retweets Engagement", "Comments Engagement"])
    with tab7:
        st.text("Likes Engagement")
        st.plotly_chart(moving_average_like_view_count(data=data, y="like_count"), theme="streamlit", use_container_width=True)
    with tab8:
        st.text("Views Engagement")
        st.plotly_chart(moving_average_like_view_count(data=data, y="view_count"), theme="streamlit", use_container_width=True)
    with tab9:
        st.text("Retweets Engagement")
        st.plotly_chart(moving_average_like_view_count(data=data, y="retweet_count"), theme="streamlit", use_container_width=True)
    with tab10:
        st.text("Comments Engagement")
        st.plotly_chart(moving_average_like_view_count(data=data, y="comments_count"), theme="streamlit", use_container_width=True)



    top_users_list, most_followed_user = top_users(data=data)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Most Number of users tweeted about {}".format(twitter_query))
        st.dataframe(top_users_list)
    
    with col2:
        st.subheader("Most Number of followers tweeted atleast Once")
        st.dataframe(most_followed_user)

    

    if sentiment_analysis == True:

        col1, col2 = st.columns(2)

        with col1:
            plot_sentiment_confidence_line(data=data)
        with col2:
            plot_sentiment_pie(data=data)


        plot_sentiment_score_line(data=data)


    st.subheader("Change of Trends in Percentage.")
    st.caption("Engagement % Change")
    col3, col4, col5, col6, col7 = st.columns(5)
    all_time_change, six_month_change, one_month_change, one_week_change, one_day_change = engagement_percentage_change(data)

    with col3:
        st.write("All Time Engagement")
        st.text(all_time_change)
    with col4:
        st.write("Six Month Engagement")
        st.text(six_month_change)
    with col5:
        st.write("One Month Engagement")
        st.text(one_month_change)
    with col6:
        st.write("One Week Engagement")
        st.text(one_week_change)
    with col7:
        st.write("One Day Engagement")
        st.text(one_day_change)
    


    column_names = ["like_count", "view_count", "retweet_count", "comments_count"]
    column_title = ["Likes", "Views", "Retweets", "Comments"]

    for i in range(len(column_names)):
        st.caption("{} % Change".format(column_title[i]))
        col8, col9, col10, col11, col12 = st.columns(5)
        counter_all_time_change, counter_six_month_change, counter_one_month_change, counter_one_week_change, counter_one_day_change = counter_percentage_change(data, column_name=column_names[i])

        with col8:
            st.write("All Time {}".format(column_title[i]))
            st.text(counter_all_time_change)
        with col9:
            st.write("Six Month {}".format(column_title[i]))
            st.text(counter_six_month_change)
        with col10:
            st.write("One Month {}".format(column_title[i]))
            st.text(counter_one_month_change)
        with col11:
            st.write("One Week {}".format(column_title[i]))
            st.text(counter_one_week_change)
        with col12:
            st.write("One Day {}".format(column_title[i]))
            st.text(counter_one_day_change)




    st.header(" ")
    st.header(" ")
    st.header(" ")
    st.header(" ")
    asset_id = get_asset_id(crypto_choice)

    st.header("Details for {}".format(crypto_choice))

    asset_details = asset_details_v2(asset_id=asset_id)


    st.subheader("Description")
    crypto_description = crypto_desc(asset_id)
    st.write(". ".join(crypto_description))

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Basic Info")
        st.text("Market Cap Rank: {}".format(asset_details["market_cap_Rank"]))
        st.text("Name: {}".format(asset_details["name"]))
        st.text("Price: {}".format(asset_details["current_price"]))
        st.text("Categories: {}".format(asset_details["categories"]))
        st.text("Hashing Algorithm: {}".format(asset_details["hashing_algorithm"]))

    with col2:

        st.subheader("Important Links")
        st.text("Homepage Link: {}".format(asset_details["homepage"]))
        st.text("Blockchain Link: {}".format(asset_details["blockchain_link"]))
        st.text("Github Link: {}".format(asset_details["github_link"]))
        st.text("Other Link: {}".format(asset_details["other_links"]))



    with col1:

        st.subheader("Price Details")
        st.text("Price: ${}".format(asset_details["current_price"]))
        st.text("ATH: ${}".format(asset_details["ath"]))
        st.text("ATL: ${}".format(asset_details["atl"]))
        st.text("ROI: {}".format(asset_details["roi"]))
        #st.text("ICO Price: {}".format(asset_details[""]))
        #st.text("ICO Date: {}".format(asset_details[""]))

    with col2:

        st.subheader("Market Data")
        st.text("Market Cap: ${}".format(asset_details["market_cap"]))
        st.text("Total Dilluted Market Cap: ${}".format(asset_details["dilution_cap"]))
        st.text("Volume: ${}".format(asset_details["volume"]))
        #st.text("Market Turnover Rate: {}".format(asset_details[]))




    with col1:

        st.subheader("Tokonomics")
        st.text("Circulating Supply: {}".format(asset_details["circulating_supply"]))
        st.text("Total Supply: {}".format(asset_details["total_supply"]))
        st.text("Max Supply: {}".format(asset_details["max_supply"]))

    with col2:

        st.subheader("Social Media")
        st.text("Twitter: {} | Followers: {}".format(asset_details["twitter_name"], asset_details["twitter_followers"]))
        st.text("Facebook: {} | Likes: {}".format(asset_details["facebook_name"], asset_details["facebook_likes"]))
        st.text("Telegram User Count: {}".format(asset_details["telegram_channel_user_count"]))
        st.text("Reddit: {} | Suscribers: {}".format(asset_details["subreddit_name"], asset_details["reddit_subscribers"]))
        st.text("Reddit Average Posts(48h): {}".format(asset_details["reddit_average_posts_48h"]))
        st.text("Reddit Average Comments(48h): {}".format(asset_details["reddit_average_comments_48h"]))
        st.text("Reddit Accounts Active(48h): {}".format(asset_details["reddit_accounts_active_48h"]))


    with col1:

        st.subheader("Score Board")
        st.text("Public UP Vote: {}".format(asset_details["up_vote"]))
        st.text("Alexa Rank: {}".format(asset_details["alexa_rank"]))
        st.text("Coingecko Rank: {}".format(asset_details["coingecko_rank"]))
        st.text("Developer Score: {}".format(asset_details["developer_score"]))
        st.text("Community Score: {}".format(asset_details["community_score"]))
        st.text("Liquidity Score: {}".format(asset_details["liquidity_score"]))

    with col2:

        st.subheader("Github Details")
        st.text("Stars: {}".format(asset_details["stars"]))
        st.text("Focks: {}".format(asset_details["forks"]))
        st.text("Total Issues: {}".format(asset_details["total_issues"]))
        st.text("Closed Issues: {}".format(asset_details["closed_issues"]))
        st.text("Pull Requests Merged: {}".format(asset_details["pull_requests_merged"]))
        st.text("Pull Request Contributors: {}".format(asset_details["pull_request_contributors"]))
        st.text("Commit Count 4 weeks: {}".format(asset_details["commit_count_4_weeks"]))


    with col1:
        
        ico_details_1 = ico_details(asset_id=asset_id)
        ico_details_2 = token_statics(asset_id=asset_id)

        st.subheader("Token ICO Info")
        st.text("ICO Price: {}".format(ico_details_1["ico_price"]))
        st.text("ICO Date: {}".format(ico_details_1["ico_date"]))
        st.text("ICO Total Tokens Sold: {}".format(ico_details_2["Total_Tokens_Sold"]))
        st.text("ICO Total Sale: {}".format(ico_details_2["Total_Sale"]))
        st.text("ICO Total Raised: {}".format(ico_details_2["Total_Raised"]))


    with col2:
        
        token_alloctaions = fetch_token_allocation(asset_id=asset_id)
        st.subheader("Token Allocations")

        for token_alloctaion in token_alloctaions:
            st.text("{}: {}".format(token_alloctaion["text"], token_alloctaion["result"]))
