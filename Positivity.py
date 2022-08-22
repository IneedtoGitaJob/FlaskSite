import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np
from GoogleNews import GoogleNews
from datetime import date
import base64
import urllib.request
import functools
import re

#Takes in a url and returns a hexidecimal value representing the average sentiment of the url page from Green representing positvive to red representing negative
def DisplayPositivity(URL)-> str:
    nltk.download("vader_lexicon")
    x = GetPositivity(URL)
    #No text
    if (x == -1):
        return("black")
    if (x == -2):
        return("Fail")
    return ("hsl("+(str)(x)+", 100%, 50%)")

def GetAveragePositivity(searchTopic, Years):
    nltk.download("vader_lexicon")
    arrOfPos = DisplayAveragePositivity(searchTopic,Years)
    print(arrOfPos)
    averagePositivity = str(np.mean(arrOfPos))
    return ("hsl("+(str)(averagePositivity)+", 100%, 50%)")

def GetPositivity(URL)-> int:
    sia = SentimentIntensityAnalyzer()
    # Find all text within paragraph tags and find the mean
    sentiment = 0.0
    num = 0
    positivity = -1
    try:
        html = urlopen(URL).read()
    except Exception as error:
        return(-2)

    soup = BeautifulSoup(html, "html.parser")
    for data in soup.find_all("p"):
        # ignore neutral sentences
        compound = sia.polarity_scores(data.get_text())['compound']
        if (compound != 0):
            num = num + 1
            sentiment = sentiment + compound
    if (num != 0):
        if (sentiment >= 0):
            positivity = (round(60 * (sentiment / num)) + 60)
        else:
            positivity = (round(60 * (sentiment / num)) * -1)
    return positivity

def _decode_google_news_url(url: str) -> str:
    #print(url)
    _ENCODED_URL_PREFIX = "news.google.com/./articles/"
    _ENCODED_URL_RE = re.compile(fr"^{re.escape(_ENCODED_URL_PREFIX)}(?P<encoded_url>[^?]+)")
    _DECODED_URL_RE = re.compile(rb'^\x08\x13".+?(?P<primary_url>http[^\xd2]+)\xd2\x01')


    match = _ENCODED_URL_RE.match(url)
    #print(match)
    encoded_text = match.groupdict()["encoded_url"]  # type: ignore
    #print(encoded_text)
    encoded_text += "==="  # Fix incorrect padding. Ref: https://stackoverflow.com/a/49459036/
    decoded_text = base64.urlsafe_b64decode(encoded_text)
    match = _DECODED_URL_RE.match(decoded_text)
    primary_url = match.groupdict()["primary_url"]  # type: ignore
    primary_url = primary_url.decode()
    return primary_url

def decode_google_news_url(url: str) -> str:
    return _decode_google_news_url(url)

def DisplayAveragePositivity(searchTopic, Years):
    #Returns a list of urls from the news
    current_year = date.today().year
    googlenews = GoogleNews()
    urlList = []
    for i in range(Years):
        googlenews = GoogleNews(start='01/01/'+(str)(current_year), end='12/31/'+(str)(current_year))
        googlenews.get_news(searchTopic)
        urlList.append(googlenews.get_links())
        current_year = current_year-1

    x = []
    numOfSuccess = 0
    pos = 0


    for y in (urlList):
        numOfSuccess = 0
        pos = 0
        print(numOfSuccess)
        for z in (y):
            try:
                pos = pos + GetPositivity(decode_google_news_url(z))
                numOfSuccess = numOfSuccess + 1
            except Exception as error:
                print(error)
        if(numOfSuccess != 0):
            x.append(round(pos/numOfSuccess))
        else:
            x.append(0)

    return x



