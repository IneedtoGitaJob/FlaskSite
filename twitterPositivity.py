from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import date
from Scweet.scweet import scrape
import re

# Get the positiivty of the search request for each year on Twitter
def getTwitterPositivity(searchRequest, Years):
    currentYear = date.today().year
    earliestYear = currentYear - Years
    sentimentTotalForEachYear = []
    sia = SentimentIntensityAnalyzer()

    # Get the positiivty of each year
    for year in range(earliestYear, currentYear, 1):
        sentimentTotalForEachYear.append(
            getYearPositivityTwitter(searchRequest, year, sia)
        )
    return sentimentTotalForEachYear


# Get the average positivity of all tweets for one year
def getYearPositivityTwitter(searchRequest, year, sia):
    data = scrape(
        words=[searchRequest],
        since=str(year) + "-01-01",
        until=str(year) + "-12-31",
        from_account=None,
        interval=80,
        headless=True,
        limit=4,
        display_type="Top",
        save_images=False,
        lang="en",
        resume=False,
        filter_replies=True,
        proximity=False,
    )
    sentimentTotal = 0.0
    count = 0

    for index, row in data.iterrows():
        sentiment = 0.0
        # Remove Noise by ignoring all numbers and special characters except for spaces
        row = re.sub("[^A-Za-z ]", "", row["Embedded_text"])

        sentiment = sia.polarity_scores(row)["compound"]

        # Dont count neutral sentences
        if sentiment != 0:
            count = count + 1
            sentimentTotal = sentimentTotal + sentiment

    # check to make sure at least one tweet was returned
    if count != 0:
        sentimentTotal = sentimentTotal / count
    else:
        sentimentTotal = 0
    # return this years total
    return sentimentTotal