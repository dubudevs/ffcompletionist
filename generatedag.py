import networkx as nx
from matplotlib import pyplot as plt
import os
import json


def generatedag():
    directory = "quests"
    quests = []
    for filename in os.listdir(directory):
        try:
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                jfile = json.load(open(f, encoding='utf8'))
                curr = jfile["quest"]["id"]
                try:
                    next = jfile["quest"]["next"]
                except:
                    next = []
                quests.append((curr, next))
        except Exception as e: 
            print(e)
            print("oops at " + str(jfile["quest"]["id"]))

    questsexpanded = []
 
    for quest in quests:
        for next in quest[1]:
            questsexpanded.append((quest[0], next))
        if(quest[1]==[]):
            questsexpanded.append((quest[0], "99999"))

    g1 = nx.DiGraph()
    g1.add_edges_from(questsexpanded)

    return g1


def get_all_pred2(node, graph):
    nodelist = []
    for pred in nx.ancestors(graph, node):
        nodelist.append(pred)
    return nodelist


def getinstancepaths():
    g1 = generatedag()
    directory = "instances"
    towrite = ""
    for filename in os.listdir(directory):
        try:
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                jfile = json.load(open(f, encoding='utf8'))
                path = ""
                path = list(dict.fromkeys(get_all_pred2(jfile["instance"]["unlockedByQuest"], g1)))
                towrite = towrite + str((jfile["instance"]["id"],path)) + "\n"
                
        except Exception as e: 
            #print(e)
            #print("oops at " + str(jfile["instance"]["id"]))
            continue
        with open("paths.txt", "w") as file:
            file.write(towrite)
    
    return


def getplayerquests():
    with open("myQuests.txt") as file:
        quests = [line.rstrip() for line in file]
    return quests


def titlefromid(id):
    jfile = json.load(open("quests/q" + str(id) + ".json", encoding='utf8'))
    return jfile["quest"]["name"]

def locfromid(id):
    jfile = json.load(open("quests/q" + str(id) + ".json", encoding='utf8'))
    return jfile["quest"]["location"]


def getdeadquests():
    directory = "quests"
    quests = []
    for filename in os.listdir(directory):
        try:
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                jfile = json.load(open(f, encoding='utf8'))
                if jfile["quest"]["reqs"]["jobs"][0]["lvl"] <= 15 or jfile["quest"]["reqs"]["jobs"][0]["lvl"] > 59 or "(" in jfile["quest"]["name"]: #or jfile["quest"]["eventIcon"] == 71201:
                    quests.append(jfile["quest"]["id"])

        except Exception as e: 
            #print(e)
            quests.append(jfile["quest"]["id"])
            continue
    
    with open("deadquests.txt", "w") as file:
        file.write(str(quests))

    return quests

def getdeadquests2():
    directory = "quests"
    quests = []
    for filename in os.listdir(directory):
        try:
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                jfile = json.load(open(f, encoding='utf8'))
                if jfile["quest"]["reqs"]["questsType"] == "any":
                    #print(jfile["quest"]["reqs"]["quests"])
                    for req in jfile["quest"]["reqs"]["quests"]:
                        quests.append(req)

        except Exception as e: 
            #quests.append(jfile["quest"]["id"])
            continue
    
    with open("deadquests.txt", "a") as file:
        file.write(str(quests))

    return quests


def getinstancepathslocal():
    with open('paths.txt', 'r') as f:
        paths = [line.rstrip() for line in f]
    return paths


def findtodo():
    graph = generatedag()
    quests = getplayerquests() + getdeadquests() + getdeadquests2()
    deadquests = getdeadquests2()
    getinstancepaths()
    paths = getinstancepathslocal()

    for i in quests:
        i = str(i)

    todo = []
    pathlist = []

    for path in paths:
        for quest in eval(path)[1]:
            if quest not in quests and str(quest) not in quests:
                todo = todo + [str(quest)]
                pathlist.append(eval(path)[0])
                break

    """print(list(dict.fromkeys(todo)))
    print(todo)
    print(pathlist)
    print(len(pathlist))
    print(len(paths)) """
    return list(dict.fromkeys(todo))



if __name__ == "__main__":
    todo = findtodo()
    for quest in todo:
        print(quest + " - " + titlefromid(quest) + " - " + locfromid(quest))