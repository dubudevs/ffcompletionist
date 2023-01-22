import requests
import bs4
import os
import json
import ast
import re

import secretfile

sess = secretfile.sess
id = secretfile.id
useweb = False

def getquestsweb():
    # Get every page of quests and soup them. Just writes the raw html for now. Returns soups
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
        "Cookie": f"ldst_touchstone=1; ldst_is_support_browser=1; ldst_sess={sess}; platform_mode=win"
    }
    page1 = requests.get(f"https://eu.finalfantasyxiv.com/lodestone/character/{id}/quest/", headers=headers).text
    page1soup = bs4.BeautifulSoup(page1)
    print(page1soup.prettify())
    lastpagelink = page1soup.select_one('a[class*="btn__pager__next--all"]')['href'].split('#', 1)[0]
    pagecount = lastpagelink.split("page=",1)[1]

    pages = []
    soups = []

    for pagenum in range(int(pagecount)):
        pages.append(requests.get(f'https://na.finalfantasyxiv.com/lodestone/character/46393163/quest/?page={pagenum + 1}#anchor_quest', headers=headers).text)
        soups.append(bs4.BeautifulSoup(pages[pagenum]))
        
    with open("pages.txt", "w", encoding="utf-8") as file:
        file.write(str(pages))

    return soups

def getquestslocal():
    # Get every page of quests from local file and soup them. Returns soups
    soups = []
    with open("pages.txt", "r", encoding="utf-8") as file:
        pages = eval(file.read())
        for page in pages:
            soups.append(bs4.BeautifulSoup(page))

    return soups

def createdict():
    # Generate the dictionary of quest name:id - doesnt need to be run unless the quests are updated
    directory = "quests"
    questdict = {}
    for filename in os.listdir(directory):
        try:
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                jfile = json.load(open(f, encoding='utf8'))
                questdict[jfile["quest"]["name"]] = jfile["quest"]["id"]
                    
        except Exception as e: 
            print(e)
            continue
    
    print(questdict)
    with open("questdict.txt", "w", encoding='utf8') as file:
        file.write(str(questdict))

    return questdict

def getdata():
    # Extract quest data from soups and write it out for later use
        if useweb:
            soups = getquestsweb()
        else:
            soups = getquestslocal()
        
        with open("questdict.txt", "r", encoding='utf8') as file:
            questdict = ast.literal_eval(file.read())

        quests = []
        queststring = ""
        for soup in soups:
            questdivs = soup.find_all("div", class_="entry__quest__name")
            for qd in questdivs:
                questname = qd.find("p").text
                questnamestrip = re.search( "\((.*)\)" ,questname).group(1).strip()
                #print(questnamestrip)
                try:
                    quests.append(questdict[questnamestrip])
                    queststring = queststring + str(questdict[questnamestrip]) + "\n"
                except Exception as e:
                    print(e)
                    continue
        with open("myQuests.txt", "w", encoding='utf8') as file:
            file.write(queststring)

def getlevel():
    # Get highest job level. Not really sure what good this is at this point tbh
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
        "Cookie": f"ldst_touchstone=1; ldst_is_support_browser=1; ldst_sess={sess}; platform_mode=win"
    }
    jobpage = requests.get(f"https://eu.finalfantasyxiv.com/lodestone/character/{id}/class_job/", headers=headers).text
    jsoup = bs4.BeautifulSoup(jobpage)
    levels = jsoup.find_all("div", {"class":"character__job__level"})
    leveltexts = [1]
    for i in levels:
        try:
            leveltexts.append(int(i.text))
        except:
            continue
    # print(max(leveltexts))
    return max(leveltexts)

if __name__ == "__main__":
    print("hi")