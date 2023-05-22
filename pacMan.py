#Update json file with new high scores
#name,score: the name and score that will be written to the file
import json

def updateScores(name, score, loc):
    #open json file and read values to a dic
    f = open("/home/DustlessSteak/mysite/static/Json/Scores.json", "r")
    #read and store
    currentScores = f.read()
    #close
    f.close()
    aList = json.loads(currentScores)

    #convert dic to list for insertion
    bList = []
    for q in aList['scores']:
        bList.append(q)

    #insert
    insertion = {'Name': name, 'Score': score}
    bList.insert(int(loc), insertion)
    #Delete the player with the lowest score
    del bList[-1]


    f2 = open("/home/DustlessSteak/mysite/static/Json/Scores.json", "w")
    f2.write("{\"scores\": "+json.dumps(bList)+"}")
    f2.close()
