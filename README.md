# CryptoKon (v1.0.1)
#### CryptoKon is a revolutionary web application that helps you stay ahead of the curve in the ever-changing world of cryptocurrency. With its advanced analysis tools, CryptoKon provides a deep understanding of the trends and movements within specific crypto projects, empowering you to make informed investment decisions. Say goodbye to sifting through endless data and hello to a streamlined, user-friendly platform that puts the power of crypto analysis at your fingertips

![Python](https://img.shields.io/badge/Python-3.9-blueviolet)
![Framework](https://img.shields.io/badge/Framework-sreamlit-red)

## Features Of CryptoKon Web App
- Can Fetch upto **10000000 Tweets**.
- Gives a **detailed Trend Analysis** of the tweets.
- Gives the most Trending Analysis to **View**, **Retweet**, **links** and **Comments** Engagement of the fetched tweets.
- Gives a seperate Analysis of **Whales account** Engagement.
- Calculating **Moving Averages**(7/14/30/60)days on the Engagement so that you can get better understanding of the trend.
- Shows **Percentage Change** of like, share, comment, views, retweets, tweets engagement in **5 interval different intervals**.
- Show a **detail information** of a perticular crypto project such as **market detail**, **Tokonomics**, **Score Board**, **Token ICO Details** and manymore.
- Manymore Features you will not regrate trying it.

### Check out the live demo: https://cryptokon.streamlit.app

### Vedio demo:
<p><img  alt="GIF" src="https://github.com/everydaycodings/Twitter-Sentimental-Analysis-WebApp/blob/master/files/app_demo.gif" width="800" height="450" /></p>

## How to run the project?

1. Clone or download this repository to your local machine.
2. Install all the libraries mentioned in the [requirements.txt](https://github.com/everydaycodings/CryptoKon/blob/master/requirements.txt) file with the command `pip3 install -r requirements.txt`
3. Open your terminal/command prompt from your project directory and run the file `app.py` by executing the command `streamlit run app.py`.
4. You will be automatically redirected the your localhost in brower where you can see you WebApp in live.

## Points To Be Noted: 
##### If you are targeting a large amount of tweets (ex: 50000 Tweets) I recommend you to do the following steps:
- Open your terminal/command prompt from your project directory and run the file `data_collector.py` by executing the command `python data_collector.py`.
- enter your query, from date you want to collect the tweets, to date you want ot collect the tweets till, and the tweets limit.
- Let the Script to run
- When the scripts says **Tweets Collection Completed**
- You can see the output folder you will get your all tweets infomation in csv files.
- Open your terminal/command prompt from your project directory and run the file `app.py` by executing the command `streamlit run app.py`.
- Upload the file to the web app and see magic.

#### A Large number of tweets fetching can sometimes crash the app. So try running the app in your localhost, and use the `data_collector.py` method to have a smooth experience.


### If you Use this Code for Any Commercial Purpose. Please Don't Forget To mention or give shoutout to [everydaycodings](https://github.com/everydaycodings).