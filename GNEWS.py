from GoogleNews import GoogleNews
import requests
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from Scweet.scweet import scrape
import re

#Calls: GetDecodedUrlPositivity
#sets up the array of urls to be processed
def multiProcessList(rawUrlList):
        #On each element call GetDecodedUrlPositivity
        with ThreadPoolExecutor(max_workers=70) as p:
            listOfAveragePositivityForEachWebsite = list(p.map(GetDecodedUrlPositivity, rawUrlList))
        return(listOfAveragePositivityForEachWebsite)

#Calls: GetPositivity
#Function called on each array element
def GetDecodedUrlPositivity(rawUrl):
    try:
        #Decode URL
        res = requests.get("http://" + str(rawUrl), timeout=5)
        #Get the positivity of the selected URL
        return(GetPositivity(res.url))
    #If we can't connect we will return an arbitrary negative number that will be filtered out later
    except Exception:
        return(-2)

#Calls: None
#Creates and returns a list of encoded URLs
def GetEncodedUrlList(searchTopic, Years):
    current_year = date.today().year
    googlenews = GoogleNews(start='01/01/'+str(current_year - Years),end='12/28/'+str(current_year))
    googlenews.get_news(searchTopic)
    rawUrlList = googlenews.get_links()
    return(rawUrlList)

#Calls: None
#Returns the positivity of a Web Page
#returns -2 for cannot connect -1 for unable to analyze text or a number 0-100 for a successful analysis
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

        #Get the positivity of the website
        for data in soup.find_all("p"):
            compound = sia.polarity_scores(data.get_text())['compound']
            # ignore neutral sentences
            if (compound != 0):
                #add 1 to count and add to sentiment total
                num = num + 1
                sentiment = sentiment + compound

        #If we were able to successfully analyze the website
        if (num != 0):
            #return as a number between 0-100
            if (sentiment >= 0):
                positivity = (round(50 * (sentiment / num)) + 50)
            else:
                positivity = (50 - (round(50 * (sentiment / num)) * -1))
        #If we were unable to connect but were unable to analyze the website we will return -1
        return positivity
    # If we can't connect we will return an arbitrary negative number that will be filtered out later
    except Exception:
        return (-2)

#Calls: GetPositivity
#Entry point for checking webpage positivity
def DisplayPositivity(URL)-> str:
    nltk.download("vader_lexicon")
    x = GetPositivity(URL)
    #No text
    if (x == -1):
        return("No Text")
    #issue connecting
    if (x == -2):
        return("Fail")
    #increase x by 20% as our HSL is on a scale from 0 to 120 and x is currently scaled 0 to 100
    x = x*1.2
    return ("hsl("+(str)(x)+", 100%, 50%)")