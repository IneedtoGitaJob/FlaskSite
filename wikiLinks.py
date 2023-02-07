import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

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
            #                                                READ THIS
            #Seach for all instances of href="/wiki/.*" title = ".*"
            #1 find -href="/wiki/- as long as the preceding words arent help or file
            #2 read until you find the next -=- but dont' include it
            #3 read the -=- and the -"-
            #4 read the text within title
            #                   1                            2   3   4
            Text = re.findall(r'href=\"\/wiki\/[^Help][^File][^=]*=\"([^\"]*)', str(data))

            #Add the Links to the wiki list
            for wikiLinkStr in Text:
                if (wikiLinkStr in dictionaryOfLinks):
                    dictionaryOfLinks[wikiLinkStr] = dictionaryOfLinks[wikiLinkStr] + 1
                else:
                    dictionaryOfLinks[wikiLinkStr] = 1
        return dictionaryOfLinks
    #If The url isn't correct
    except Exception:
        return ("Fail")