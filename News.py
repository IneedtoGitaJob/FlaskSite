import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import multiprocessing

def getNews(URL):
    sia = SentimentIntensityAnalyzer()
    #Find all text within paragraph tags and find the mean
    sentiment = 0.0
    num = 0
    positivity = -1
    html = urlopen(URL).read()
    soup = BeautifulSoup(html, "html.parser")
    for data in soup.find_all("p"):
        # ignore neutral sentences
        compound = sia.polarity_scores(data.get_text())['compound']
        if(compound != 0):
            num = num + 1
            sentiment = sentiment + compound
    if (num != 0):
        if(sentiment >= 0):
            positivity = (round(60 * (sentiment / num)) + 60)
        else:
            positivity = (round(60 * (sentiment / num))*-1)
    return positivity
