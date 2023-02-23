from flask import Flask, render_template, request, jsonify
from GNEWS import DisplayPositivity, getUrls, getPositivityNews
from twitterPositivity import getTwitterPositivity
from wikiLinks import getWikiLinks
from pacMan import updateScores
import json

app = Flask(__name__)

# index
@app.route("/")
def index():
    return render_template("index.html")


# WebPositivity
@app.route("/WebPositivity")
def WebPositivity():
    return render_template("WebPositivity.html")


# pacman
@app.route("/pacMan")
def pacMan():
    return render_template("pacMan.html")


# pacman file write
@app.route("/pacManUpdateScores", methods=["POST"])
def pacManWebProcess():
    nameToBeChanged = request.form["nameToBeChanged"]
    scoreToBeChanged = request.form["scoreToBeChanged"]
    name = request.form["name"]
    score = request.form["score"]
    loc = request.form["loc"]
    updateScores(nameToBeChanged, scoreToBeChanged, name, score, loc)
    return "1"


# Wiki
@app.route("/Wiki")
def Wiki():
    return render_template("wikiLinks.html")


# Get Positivity of a Website
@app.route("/backgroundWebProcess", methods=["POST"])
def backgroundWebProcess():
    URL = request.form["text"]
    return DisplayPositivity(URL)


# Get Positivity of a series News stories
@app.route("/backgroundNewsProcessMulti", methods=["POST"])
def backgroundManyWebProcessMulti():
        searchTopic = request.form["text"]
        Years = request.form["Years"]

        # list of Average Positivities for each News Year
        averagePositivity = []

        # Get list of urls to be checked
        urlList = getUrls(searchTopic, int(Years))

        # Input: encoded List of encoded Urls
        # Process 1: connects to each url
        # Process 2: Gets Positivity of each url
        # Output: List of all the positivities within the news year range
        averagePositivity = getPositivityNews(urlList)

        # Remove all articles that failed to connect or that had no text
        averagePositivity = [pos for pos in averagePositivity if pos > 0]

        # If we failed to find any News Stories return a Fail
        if len(averagePositivity) == 0:
            return "Fail"
        #Else stringify average positivity and return
        return " ".join(str(x) for x in averagePositivity)



# Return a Json of Wikipedia Links
@app.route("/wikiLinksProcess", methods=["POST"])
def wikiLinksProcess():
    searchRequest = request.form["searchRequest"]
    jsonWikiLinks = json.dumps(getWikiLinks(searchRequest), indent=0)
    return jsonWikiLinks


# Return a Json of twitter positivities
@app.route("/twitterProcess", methods=["POST"])
def twitterProcess():
    searchRequest = request.form["text"]
    Years = request.form["Years"]
    return jsonify(getTwitterPositivity(searchRequest, int(Years)))


# Debugmode
if __name__ == "__main__":
    app.run(debug=True)
