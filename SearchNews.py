from GoogleNews import GoogleNews
from datetime import date
import urllib.request
import functools
from multiprocessing import Pool
from multiprocessing import cpu_count
import time
from urllib.request import urlopen
import numpy as np
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup

#Returns a list of urls from the news
def GetNewsUrls(searchTopic, Years):
    current_year = date.today().year
    urlList = []

    for x in range(Years):
        #for y in range(1):
        googlenews = GoogleNews(start= '1/01/'+(str)(current_year), end= '12/30/'+(str)(current_year))
        googlenews.search(searchTopic)
        time.sleep(3)
        result = googlenews.get_links()
        #if result is not None:
        urlList.append(result)
        current_year = current_year-1
    return (urlList)

#sets up the array of urls to be multiprocessed
def multiProcessList(y):
    with Pool() as p:
        tempList = list(p.map(CallPositivity, y))
    return(tempList)

#Function called on each array
def CallPositivity(x):
    try:
        return(GetPositivity(x))
    except Exception as error:
        return(0)

#Returns the average positivity of all the URLS
def ProcessURLS(urList):
    averagePositivity = []

    for z in urList:

        for y in z:
            print(y)
            q = GetPositivity(y)
            print (q)
            averagePositivity.append(np.mean(q))

    return(averagePositivity)

#Entry point
def GetAverageURLSPositivity(searchTopic, Years):
    nltk.download("vader_lexicon")
    urlList = GetNewsUrls(searchTopic, Years)
    averagePositivity = ProcessURLS(urlList)
    absolutePos = []
    for i in averagePositivity:
        if(i > 0):
            absolutePos.append(i)
    x = np.mean(absolutePos)
    return ("hsl("+(str)(x)+", 100%, 50%)")

#Entry point
def DisplayPositivity(URL)-> str:
    nltk.download("vader_lexicon")
    x = GetPositivity(URL)
    #No text
    if (x == -1):
        return("black")
    #issue connecting
    if (x == -2):
        return("Fail")
    return ("hsl("+(str)(x)+", 100%, 50%)")

#Returns the positivity of an article
def GetPositivity(URL)-> int:
    sia = SentimentIntensityAnalyzer()
    # Find all text within paragraph tags and find the mean
    sentiment = 0.0
    num = 0
    positivity = -1
    try:
        html = urlopen(URL).read()
    except Exception as error:
        print(error)
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

"""
averagePositivity = []

for z in urlList:
    print(z)
    if __name__ == '__main__':
        q = multiProcessList(z)
        print(q)
        averagePositivity.append(np.mean(q))
print(averagePositivity)
"""