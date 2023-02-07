from flask import Flask, render_template,request,jsonify
from GNEWS import DisplayPositivity,GetEncodedUrlList,multiProcessList
from twitterPositivity import getTwitterPositivity
from wikiLinks import getWikiLinks
import json

app = Flask(__name__)

#index
@app.route('/')
def index():
    return render_template('index.html')

#WebPositivity
@app.route('/WebPositivity')
def WebPositivity():
    return render_template('WebPositivity.html')

#pacman
@app.route('/pacMan')
def pacMan():
    return render_template('pacMan.html')

#Wiki
@app.route('/Wiki')
def Wiki():
    return render_template('wikiLinks.html')

#Get Positivity of a Website
@app.route('/backgroundWebProcess', methods=['POST'])
def backgroundWebProcess():
    URL = request.form["text"]
    return (DisplayPositivity(URL))

#Get Positivity of a series News stories
@app.route('/backgroundNewsProcessMulti', methods=['POST'])
def backgroundManyWebProcessMulti():
    if __name__ == "__main__":
        searchTopic = request.form["text"]
        Years = request.form["Years"]

        # list of Average Positivities for each News Year
        averagePositivity = []

        # GetEncoded URList, URLs are considered encoded as they aren't a link and must be processed later
        EncodedurlList = GetEncodedUrlList(searchTopic, int(Years))

        # Input: encoded List of Urls
        # Process 1: decodes list of Urls
        # Process 2: Gets Positivity of Urls
        # Output: List of all the positivities of all News years
        averagePositivity = multiProcessList(EncodedurlList)

        # Remove all articles that failed to connect or that had no text
        averagePositivity = [pos for pos in averagePositivity if pos > 0]

        #If we failed to find any News Stories return a Fail
        if(len(averagePositivity)==0):
            return("Fail")
        return (" ".join(str(x) for x in averagePositivity))

    #If we are Not Running on main Fail as we need to use multithreading
    return("Fail")

#Return a Json of Wikipedia Links
@app.route('/wikiLinksProcess', methods=['POST'])
def wikiLinksProcess():
    searchRequest = request.form["searchRequest"]
    jsonWikiLinks = json.dumps(getWikiLinks(searchRequest), indent=0)
    return (jsonWikiLinks)

#Return
@app.route('/twitterProcess', methods=['POST'])
def twitterProcess():
    searchRequest = request.form["text"]
    Years = request.form["Years"]
    return jsonify(getTwitterPositivity(searchRequest, int(Years)))

#Debugmode
if __name__ == "__main__":
    app.run(debug=True)
