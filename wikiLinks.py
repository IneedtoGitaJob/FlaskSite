import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import json
import time
# WIP
# return an img url of an img that appears on the wiki page
# html: the html of the wiki page
# return: url of img
def convertWikipediaLinkToImageLink(html):
    start_time = time.time()
    soup = BeautifulSoup(html, "html.parser")

    # Try and find the img commonly used on wikipedia articles by the decoding attribute that they usually contain
    imgToBeLinked = soup.find(
        lambda tag: tag.name == "img" and (tag.has_attr("decoding") and int(tag["width"]) > 100)
    )
    # If we cant find an image just link to a black square
    if imgToBeLinked is None:
        return "https://commons.wikimedia.org/wiki/File:Black_square.jpg"
    else:
        imgLink = re.search(r'src="([^"]*)', str(imgToBeLinked))
    print(f' process takes {time.time() - start_time} seconds')
    return "https:" + imgLink.group(1)


# Open and read the html of a page and return the html
# urlEnd: The ending of the url for https://en.wikipedia.org/wiki/urlEnd
# return: the html of the webpage or "Fail" if the webpage doesn't exist
def readHtml(urlEnd):
    try:
        # Open WikiPage and read HTML
        req = urllib.request.Request(
            ("https://en.wikipedia.org/wiki/" + str(urlEnd)),
            data=None,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
            },
        )
        requester = urlopen(req)
        html = requester.read()
        requester.close()

        return html
    # If The url isn't correct
    except Exception:
        return "Fail"


# Get all of the refrences within the text of a wikipedia page
# searchRequest: The wikipedia page to be searched
# Return: dictionary of references in the following schema: {"reference":count}
def getWikiLinks(searchRequest):

    dictionaryOfLinks = {}

    html = readHtml(searchRequest)
    if html == "Fail":
        return "Fail"
    soup = BeautifulSoup(html, "html.parser")

    # For every paragraph retrive the href titles and add them to the dictionary
    for data in soup.find_all("p"):
        # href=\"\/wiki\/([^Help][^File][^"]*)" title="([^\"]*)
        # Get the title contents of all a tags in paragraphs
        # Seach for all instances of href="/wiki/.*" title = ".*"
        # 1 find -href="/wiki/.*" title="- as long as the preceding words arent help or file
        # 2 read the text within title
        Text = re.findall(
            r'href=\"\/wiki\/[^Help][^File][^"]*" title="([^\"]*)', str(data)
        )
        # Add the Links to the dict for every duplicate link instead add to the count
        # Linkname[1] is the name as it appears on wikipedia linkname[2] is the name of the corresponding url link
        for linkName in Text:
            # if we already have the link add one to the count
            if linkName in dictionaryOfLinks:
                dictionaryOfLinks[linkName] = dictionaryOfLinks[linkName] + 1
            # else create a new entry
            else:
                dictionaryOfLinks[linkName] = 1
    dictionaryOfLinks["imgLinkToaddtoChart"] = convertWikipediaLinkToImageLink(html)
    # convertWikipediaLinkToImageLink(dictionaryOfLinks)
    return dictionaryOfLinks

getWikiLinks("Cheese")