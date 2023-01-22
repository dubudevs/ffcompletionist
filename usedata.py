import networkx as nx
from matplotlib import pyplot as plt
import os
import json
import getplayerdata

def generatedag():
    # Generate the Directional Acyclic Graph of all quests and their relations. The final quest in the line will be a requirement for quest 99999 (todo).
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
    # Get all ancestors (requirement path) of a node. Ordered.
    nodelist = []
    for pred in nx.ancestors(graph, node):
        nodelist.append(pred)
    return nodelist


def getinstancepaths():
    # Get the full ordered requirement path for all "instances"
    # Todo: Generalise
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
    # Read the local quests file into a list
    with open("myQuests.txt") as file:
        quests = [line.rstrip() for line in file]
    return quests


def titlefromid(id):
    # Get the name of a quest from its ID
    jfile = json.load(open("quests/q" + str(id) + ".json", encoding='utf8'))
    return jfile["quest"]["name"]

def locfromid(id):
    # Get the location of a quest from its ID
    jfile = json.load(open("quests/q" + str(id) + ".json", encoding='utf8'))
    return jfile["quest"]["location"]


def getlevel():
    # This makes a web request and returns highest job level
    getplayerdata.getlevel()
    return getplayerdata.getlevel()

def getdeadquests():
    # Some quests are useless/cause issues, all sub level 15 quests are assumed as are quests with ( in the name, eg (Twin Adder) and (Flame Immortal)
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
    # Consider quests that require one of "any" quest completed
    # Todo: Find a decent way to implement this in networkx
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
    # Read instance quest paths from local file rather than generating them
    with open('paths.txt', 'r') as f:
        paths = [line.rstrip() for line in f]
    return paths


def findtodo():
    # Move up every instance's tree starting from level 1 and find the first uncompleted quest. Considers "dead quests" completed.
    quests = getplayerquests() + getdeadquests() + getdeadquests2() + getdupes()
    # graph = generatedag()
    # deadquests = getdeadquests2()
    # getinstancepaths()
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


def getdupes():
    # There are a couple of quests that share the same name. From the scraped data it is very hard to differentiate these. Consider dupes dead for now.
    # Todo: Differentiate, possibly by icons
    directory = "quests"
    quests = []
    dupeid = []
    for filename in os.listdir(directory):
        try:
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                jfile = json.load(open(f, encoding='utf8'))
                quests.append(jfile["quest"]["name"])

        except Exception as e: 
            print(e)
            continue
    
    dupes=[i for i in quests if quests.count(i)>1]
    print(dupes)

    for filename in os.listdir(directory):
        try:
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                jfile = json.load(open(f, encoding='utf8'))
                if jfile["quest"]["name"] in dupes:
                    dupeid.append(jfile["quest"]["id"])

        except Exception as e: 
            print(e)
            continue

    print(dupeid)

    #with open("dupe.txt", "w") as file:
    #    file.write(str(dupeid))

    return dupeid


if __name__ == "__main__":

    todo = findtodo()
    garland =  "https://garlandtools.org/db/#"
    for quest in todo:
        print(quest + " - " + titlefromid(quest) + " - " + locfromid(quest))
        garland = garland + f"quest/{quest},"
    print(garland[:-1])