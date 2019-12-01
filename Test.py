from urllib.request import Request, urlopen
import ssl
from bs4 import BeautifulSoup
import json
import requests

game_name = "Journey"
the_URL = "https://chicken-coop.fr/rest/games/"+str(game_name)+"?"
# https://chicken-coop.fr/rest/games/[TITLE]?platform=[PLATFORM]&amp;selectors[]=title&amp;selectors[]=genre&amp;selectors[]=score&amp;selectors[]=alsoAvailableOn&amp;selectors[]=image&amp;selectors[]=description
response = requests.get(the_URL)
print(response.json())
todos = json.loads(response.text)
print(todos)
print(type(todos))
print(todos['result'])
print(todos['result']['genre'])
print(todos['result']['title'])

# context = ssl._create_unverified_context()
# req = Request(str(the_URL), headers={'User-Agent': 'Mozilla/5.0'})
# get_SER = urlopen(req, context=context).read()
# soup = BeautifulSoup(get_SER, features="html.parser")

# print(soup.find('title'))

# soup = BeautifulSoup(get_SER, features="html.parser")
# find_all_clamp_summary_wrap = soup.find_all('h3')
#
# find_all_meta_score = soup.find_all("div", class_="metascore_w large game positive")
