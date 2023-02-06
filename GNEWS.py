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
from flask import jsonify

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
    except Exception:
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
            compound = sia.polarity_scores(data.get_text())['compound']
            # ignore neutral sentences
            if (compound != 0):
                #add 1 to count and add to sentiment total
                num = num + 1
                sentiment = sentiment + compound
        #If we were able to successfully analyze at least one website
        if (num != 0):
            if (sentiment >= 0):
                positivity = (round(50 * (sentiment / num)) + 50)
            else:
                positivity = (50 - (round(50 * (sentiment / num)) * -1))

        return positivity
    except Exception:

        return (-2)

def getTwitterPositivity(searchRequest, Years):
    currentYear = date.today().year
    earliestYear = currentYear-Years
    sentimentTotalForEachYear = []
    sia = SentimentIntensityAnalyzer()
    for year in range(earliestYear, currentYear, 1):
        sentimentTotalForEachYear.append(getYearPositivity(searchRequest,year,sia))
    return jsonify(sentimentTotalForEachYear)

def getYearPositivity(searchRequest,year,sia):
        data = scrape(
        words=[searchRequest], since= str(year)+"-01-01", until=str(year)+"-12-31", from_account=None, interval=60,
        headless=True,limit = 10, display_type="Top", save_images=False, lang="en",
        resume=False, filter_replies=True, proximity=False
                     )
        sentimentTotal = 0.0
        count = 0

        for index, row in data.iterrows():
            sentiment = 0.0
            #Remove Noise
            row = re.sub('[^A-Za-z ]', '', row['Embedded_text'])

            sentiment = sia.polarity_scores(row)['compound']

            #Dont count neutral sentences
            if(sentiment != 0):
                count = count + 1
                sentimentTotal = sentimentTotal + sentiment

        #check to make sure at least one tweet was returned
        if(count != 0):
            sentimentTotal = sentimentTotal/count
        else:
            sentimentTotal = 0
        #return this years total
        return(sentimentTotal)

def getWikiLinks(searchRequest):
    try:

        #Open WikiPage and read HTML
        req = urllib.request.Request(
            ("https://en.wikipedia.org/wiki/"+str(searchRequest)),
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        requester = urlopen(req)
        html = requester.read()
        requester.close()
        soup = BeautifulSoup(html, "html.parser")

        dictionaryOfLinks = {}

        #For every paragraph retrive the href titles and add them to the dictionary
        for data in soup.find_all("p"):

            Text = re.findall(r'href=\"\/wiki\/[^Help][^File][^=]*=\"([^\"]*)', str(data))

            for wikiLinkStr in Text:
                if (wikiLinkStr in dictionaryOfLinks):
                    dictionaryOfLinks[wikiLinkStr] = dictionaryOfLinks[wikiLinkStr] + 1
                else:
                    dictionaryOfLinks[wikiLinkStr] = 1
        return dictionaryOfLinks
    except Exception:
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