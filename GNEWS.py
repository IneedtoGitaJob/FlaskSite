import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date
import asyncio
import aiohttp
from googlesearch import search
import time

#Fetch the html of a single url
async def fetch(session, url):
    try:
        async with session.get(url, timeout=5,            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
            }) as response:
            return await response.text()
    except Exception:

        return("Fail")


#Settup Async tasks and Fetch the html of every webpage by calling fetch on it
async def fetchAll(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(fetch(session, url))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        return responses

# Creates and returns a list of URLs
def getUrls(searchRequest, years):
    listOfUrls = []
    currentYear = date.today().year
    earliestYear = str(currentYear - years)
    #iterate over Search request
    for url in search((searchRequest+" after:"+earliestYear+"-01-01"), num_results=40):
        listOfUrls.append(url)
    return listOfUrls

#start event loop to asynchronously connect to urls and then iterate over the responses to find the positivites
def getPositivityNews(urls):
    positivities = []
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    responses = loop.run_until_complete(fetchAll(urls))
    time.sleep(0.1)
    sia = SentimentIntensityAnalyzer()

    for html in responses:
        positivities.append(getPositivity(html, sia))
    return positivities

def getPositivity(html,sia):
    sentiment = 0.0
    num = 0
    positivity = -1
    soup = BeautifulSoup(html, "html.parser")
    # Get the positivity of the website
    for data in soup.find_all("p"):
        compound = sia.polarity_scores(data.get_text())["compound"]
        # ignore neutral sentences
        if compound != 0:
            # add 1 to count and add to sentiment total
            num = num + 1
            sentiment = sentiment + compound

    # If we were able to successfully analyze the website
    if num != 0:
        # return as a number between 0-100
        if sentiment >= 0:
            positivity = round(50 * (sentiment / num)) + 50
        else:
            positivity = 50 - (round(50 * (sentiment / num)) * -1)
    # If we were able to connect but were unable to analyze the website we will return -1
    return positivity


# Calls: None
# Returns the positivity of a Web Page
# returns -2 for cannot connect -1 for unable to analyze text or a number 0-100 for a successful analysis
def GetPositivity(URL) -> int:

    try:
        sia = SentimentIntensityAnalyzer()
        sentiment = 0.0
        num = 0
        positivity = -1

        # Set Headers
        req = urllib.request.Request(
            URL,
            data=None,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
            },
        )

        requester = urlopen(req)
        html = requester.read()
        requester.close()
        soup = BeautifulSoup(html, "html.parser")

        # Get the positivity of the website
        for data in soup.find_all("p"):
            compound = sia.polarity_scores(data.get_text())["compound"]
            # ignore neutral sentences
            if compound != 0:
                # add 1 to count and add to sentiment total
                num = num + 1
                sentiment = sentiment + compound

        # If we were able to successfully analyze the website
        if num != 0:
            # return as a number between 0-100
            if sentiment >= 0:
                positivity = round(50 * (sentiment / num)) + 50
            else:
                positivity = 50 - (round(50 * (sentiment / num)) * -1)
        # If we were unable to connect but were unable to analyze the website we will return -1
        return positivity
    # If we can't connect we will return an arbitrary negative number that will be filtered out later
    except Exception:
        return -2


# Calls: GetPositivity
# Entry point for checking webpage positivity
def DisplayPositivity(URL) -> str:
    nltk.download("vader_lexicon")
    x = GetPositivity(URL)
    # No text
    if x == -1:
        return "No Text"
    # issue connecting
    if x == -2:
        return "Fail"
    # increase x by 20% as our HSL is on a scale from 0 to 120 and x is currently scaled 0 to 100
    x = x * 1.2
    return "hsl(" + (str)(x) + ", 100%, 50%)"