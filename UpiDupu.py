from GoogleNews import GoogleNews
from datetime import date
from News import getNews
import base64
import urllib.request
import functools
import re
import requests

#Returns a list of urls from the news
numyears = 1
current_year = date.today().year
googlenews = GoogleNews()
urlList = []
for x in range(numyears):
    googlenews = GoogleNews(start='01/01/'+(str)(current_year), end='12/31/'+(str)(current_year))
    googlenews.get_news('APPLE')
    urlList.append(googlenews.get_links())
    current_year = current_year-1

for y in (urlList):
    for z in (y):
        z = "http://"+z
        print(z)
        getNews(z)
        print("ga")
        """
        s = z.replace('news.google.com/./articles/','')
        q = s.replace('hl=en-US&gl=US&ceid=US%3Aen','')
        f = q.replace(q[-1],'')
        (f.len/4)
        f += "=="
        url = base64.b64decode(f)
        print(url)
        """

"""
for y in (urlList):
    for z in (y):
        try:
            coded = 'CBMiUGh0dHBzOi8vd3d3LnBva2VybmV3cy5jb20vc3RyYXRlZ3kvd3NvcC1tYWluLWV2ZW50LXRpcHMtbmluZS1jaGFtcGlvbnMtMzEyODcuaHRt0gEA'
            url = base64.b64decode(coded)
            print(url)
            z += '==='
            print(decode_google_news_url(z))
        except Exception as error:
            print("Failed")
"""



