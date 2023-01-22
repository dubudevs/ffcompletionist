# ffcompletionist
A WIP (but functional) tool to tell YOU what quests to complete to unlock everything

Fetch your data using getplayerdata.py (you'll need to figure out which functions you want for now) and then use usedata.py to generate a list of quests to do and a GT link for easy reading.

# Todo
- ~~Fetch quests and levels from API (requires scraping and cookie wrangling)~~
- Use a single API rather than two for fetching data
- Find/fix bugs
- ~~Visualisation~~
- Interactive web app
- More than just instances
- Fix ( hack
- Fix "any" hack
- Generalise getinstancepaths()
- is 99999 a problem?

# Completed todo
- Fetch character's quests from Lodestone - requires setting character id and session cookie in secretfile.py (check cookies in browser, must be logged in - ldst_sess)
- Levels can be scraped, but I dont think I will do anything with them
- Garland Tools lists work as a very nice way to visualise
