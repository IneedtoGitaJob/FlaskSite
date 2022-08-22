from GoogleNews import GoogleNews
from datetime import date
from Positivity import GetPositivity
import base64
import urllib.request
import functools
import re
from multiprocessing import Pool
from multiprocessing import cpu_count
import time
from urllib.request import urlopen

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
    for x in range(Years):
        googlenews = GoogleNews(start='01/01/'+(str)(current_year), end='12/31/'+(str)(current_year))
        googlenews.get_news(searchTopic)
        urlList.append(googlenews.get_links())
        current_year = current_year-1

    x = []
    numOfSuccess = 0
    pos = 0
    q = []

    for y in (urlList):
        q = multiProcessList(y)
        print(q)


    return q

def multiProcessList(y):
    if __name__ == '__main__':
        with Pool(cpu_count()) as p:
         return(p.map(CallPositivity, y))
def CallPositivity(x):
    try:
        return GetPositivity(decode_google_news_url(x))
    except Exception as error:
        print(error)

def OoogaBooga(searchTopic, Years):
    current_year = date.today().year
    googlenews = GoogleNews()
    urlList = []

    for x in range(Years):
        for y in range(12):
            googlenews = GoogleNews(start= str(y)+'/01/'+(str)(current_year), end= str(y)+'/28/'+(str)(current_year))
            googlenews.search(searchTopic)
            print(googlenews.get_links())
            urlList.append(googlenews.get_links())
        current_year = current_year-1
    print(urlList)




start_time = time.time()
OoogaBooga("Israel", 1)
print("--- %s seconds ---" % (time.time() - start_time))