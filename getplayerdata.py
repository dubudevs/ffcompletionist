import requests
import bs4

import secretfile

sess = secretfile.sess

def getquests(id):
    headers = {f"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
"Cookie": "ldst_touchstone=1; ldst_is_support_browser=1; ldst_sess={sess}; platform_mode=win"
}
    page1 = requests.get("https://eu.finalfantasyxiv.com/lodestone/character/{id}/quest/", headers=headers).text
    page1soup = bs4.BeautifulSoup(page1)
    print(page1soup.prettify())
    print(page1soup.select_one('a[class*="btn__pager__next--all"]'))

getquests(secretfile.id)