#Update json file with new high scores
#nameToBeChanged,scoreTobeChanged,loc: used to locate at what location we change our json
#name,score: the name and score that will be written to the file
def updateScores(nameToBeChanged, scoreToBeChanged, name, score, loc):
    #open json file
    f = open("/home/DustlessSteak/mysite/static/Json/Scores.json", "r")
    #read and store
    currentScores = f.read()
    #close
    f.close()
    #erase file contents and open
    f = open("/home/DustlessSteak/mysite/static/Json/Scores.json", "w")
    # Replace the target string
    currentScores = currentScores.replace('''  {
   "No": "'''+loc+'''",
   "Name": "'''+nameToBeChanged+'''",
   "Score": "'''+scoreToBeChanged+'''"
  }''', '''  {
   "No": "'''+loc+'''",
   "Name": "'''+name+'''",
   "Score": "'''+score+'''"
  }''')
    #update file
    f.write(currentScores)
    #close
    f.close()

#TEST
#updateScores("Carlos","77","bob","10","1")