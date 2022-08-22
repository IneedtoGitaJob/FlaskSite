import win32api
from flask import Flask, render_template,request
from SearchNews import GetAverageURLSPositivity
from SearchNews import DisplayPositivity
import json

app = Flask(__name__)


#Using the below, the popup message appears on the page load of index.html
#0x00001000 - This makes the popup appear over the browser window
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/WebPositivity')
def WebPositivity():
    return render_template('WebPositivity.html')

#Get Positivity Of a Website
@app.route('/backgroundWebProcess', methods=['POST'])
def backgroundWebProcess():
    URL = request.form["text"]
    return (DisplayPositivity(URL))

#Get Positivity of News stories
@app.route('/backgroundNewsProcess', methods=['POST'])
def backgroundManyWebProcess():
    searchTopic = request.form["text"]
    Years = request.form["Years"]
    return (GetAverageURLSPositivity(searchTopic, (int)(Years)))


if __name__ == "__main__":
    app.run(debug=True)