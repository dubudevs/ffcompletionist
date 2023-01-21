import requests
import json

def fetchquests():
    qinit = requests.get("https://xivapi.com/Quest").json()
    total = qinit["Pagination"]["ResultsTotal"]
    first = 65536

    for i in range(total): 
        try:
            url = "https://garlandtools.org/api/get.php"
            params = dict(
                id=str(first + i),
                type='quest',
                lang='en',
                version='2'
            )
            
            resp = requests.get(url=url, params=params)

            filename = "./quests/q" + str(first + i) + ".json"

            if(resp.json()):
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(resp.json(), f, ensure_ascii=False, indent=4)
            else:
                print(filename + " blank")
            #print(resp.json())
        except:
            print("Failed at " + filename)


def fetchinstances():
    qinit = requests.get("https://xivapi.com/InstanceContent").json()
    Pages = qinit["Pagination"]["PageTotal"]

    insts = []

    for page in range(Pages):
        thispage = requests.get("https://xivapi.com/InstanceContent?page=" + str(page+1)).json()
        for inst in thispage["Results"]:
            insts.append(str(inst["ID"]))

    print(insts)

    for i in range(len(insts)): 
        try:
            url = "https://garlandtools.org/api/get.php"
            params = dict(
                id=str(insts[i]),
                type='instance',
                lang='en',
                version='2'
            )
            
            resp = requests.get(url=url, params=params)

            filename = "./instances/i" + str(insts[i]) + ".json"

            if(resp.json()):
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(resp.json(), f, ensure_ascii=False, indent=4)
            else:
                print(filename + " blank")
            #print(resp.json())
        except:
            print("Failed at " + filename)