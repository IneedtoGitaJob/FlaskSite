from GoogleNews import GoogleNews
import datetime
import requests
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from datetime import date

#Calls: GetDecodedUrlPositivity
#sets up the array of urls to be processed
def multiProcessList(rawUrlList):
        with ThreadPoolExecutor(max_workers=70) as p:
            tempList = list(p.map(GetDecodedUrlPositivity, rawUrlList))
        return(tempList)

#Calls: GetPositivity
#Function called on each array
def GetDecodedUrlPositivity(rawUrlList):
    try:
        #Decode URLs
        res = requests.get("http://" + str(rawUrlList), timeout=5)
        return(GetPositivity(res.url))
    except Exception as error:
        return(-2)

#Calls: None
#Returns a list of encoded URLs
def GetEncodedUrlList(searchTopic, Years):
    current_year = date.today().year
    googlenews = GoogleNews(start='01/01/'+str(current_year - Years),end='12/28/'+str(current_year))
    googlenews.get_news(searchTopic)
    rawUrlList = googlenews.get_links()
    return(rawUrlList)

#Calls: None
#Returns the positivity of a Web Page
def GetPositivity(URL)-> int:

    try:
        sia = SentimentIntensityAnalyzer()
        sentiment = 0.0
        num = 0
        positivity = -1

        #Set Headers
        req = urllib.request.Request(
            URL,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )

        requester = urlopen(req)
        html = requester.read()
        requester.close()
        soup = BeautifulSoup(html, "html.parser")

        for data in soup.find_all("p"):
            # ignore neutral sentences
            compound = sia.polarity_scores(data.get_text())['compound']
            if (compound != 0):
                num = num + 1
                sentiment = sentiment + compound
        if (num != 0):
            if (sentiment >= 0):
                positivity = (round(50 * (sentiment / num)) + 50)
            else:
                positivity = (50 - (round(50 * (sentiment / num)) * -1))
        #print("-------------------Positivity: "+ str(positivity)+ "     URL:" + str(URL))
        return positivity
    except Exception as error:
        #print(error)
        return (-2)

#Calls: GetPositivity
#Entry point for checking webpage positivity
def DisplayPositivity(URL)-> str:
    nltk.download("vader_lexicon")
    x = GetPositivity(URL)
    #No text
    if (x == -1):
        return("black")
    #issue connecting
    if (x == -2):
        return("Fail")
    #increase x by 20% as our HSL is on a scale from 0 to 120 and x is currently scaled 0 to 100
    x = x*1.2
    return ("hsl("+(str)(x)+", 100%, 50%)")