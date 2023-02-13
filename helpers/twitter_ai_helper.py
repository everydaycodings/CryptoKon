import pandas as pd
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import plotly.express as px
import streamlit as st
from textblob import TextBlob


roberta = "cardiffnlp/twitter-roberta-base-sentiment-latest"
model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)


def getPolarity(text):

   polarity = TextBlob(text).sentiment.polarity
   return format('%.2f' %float(polarity))


def sentiment_score(tweet):

    sentiment_task = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    sentiment = sentiment_task(tweet)[0]
    return format('%.2f' %float(sentiment["score"]))


def sentiment_label(tweet):

    sentiment_task = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    sentiment = sentiment_task(tweet)[0]
    return sentiment["label"]


def add_sentiment_score_labels(data):

    data["sentiment_confidence"] = data["Tweet"].apply(sentiment_score)
    data["sentiment_label"] = data["Tweet"].apply(sentiment_label)

    return data


def get_sentiment_polarity(data):

    data['sentiment_score'] = data['Tweet'].apply(getPolarity)

    return data



def plot_sentiment_pie(data):
    
    sentiment_label = data.groupby(["sentiment_label"]).size().reset_index(name="number of engagements")
    fig = px.pie(sentiment_label, values='number of engagements', names='sentiment_label')
    fig.update_layout(title="Distribution of Sentiment")

    return st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def plot_sentiment_confidence_line(data):
    
    sentiment_label = data.groupby("Date")["sentiment_confidence"].agg(["mean", "size"]).reset_index()
    sentiment_label.rename(columns={"mean": "Sentiment Confidence", "size": "Number Of Engagements"}, inplace=True)
    fig = px.line(sentiment_label, x="Date", y="Sentiment Confidence", hover_data=["Number Of Engagements"])
    fig.update_layout(title="Confidence of the Sentiments on a perticular Date")
    fig.add_hline(y=0.9, line_dash="dot", line_color="green", annotation_text="Very High Sentiment Confidence")
    fig.add_hline(y=0.5, line_dash="dot", line_color="yellow", annotation_text="Neutal Sentiment Confidence")
    fig.add_hline(y=0.1, line_dash="dot", line_color="red", annotation_text="Low Sentiment Confidence")
    
    return st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def plot_sentiment_score_line(data):
    
    sentiment_label = data.groupby("Date")["sentiment_score"].agg(["mean", "size"]).reset_index()
    sentiment_label.rename(columns={"mean": "Sentiment Score", "size": "Number Of Engagements"}, inplace=True)
    fig = px.line(sentiment_label, x="Date", y="Sentiment Score", hover_data=["Number Of Engagements"])
    fig.update_layout(title="Average Distribution of Sentiments on a perticular Date")
    fig.add_hline(y=1, line_dash="dot", line_color="green", annotation_text="Highly Positive Sentiment")
    fig.add_hline(y=0.0, line_dash="dot", line_color="yellow", annotation_text="Neutal Sentiment")
    fig.add_hline(y=-1, line_dash="dot", line_color="red", annotation_text="Highly Negative Sentiment")
    
    return st.plotly_chart(fig, theme="streamlit", use_container_width=True)