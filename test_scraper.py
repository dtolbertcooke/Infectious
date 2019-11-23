import requests
from bs4 import BeautifulSoup as SOUP
import csv
import re

'''
orig_url = 'https://www.metacritic.com/browse/games/genre/metascore/action/all?view=detailed'
# added headers to 'webpage' variable bc webpage security returned 403 error
webpage = requests.get(orig_url, headers={'User-Agent': 'Mozilla/5.0'})
soup = SOUP(webpage.text, 'html.parser')
'''

# f = csv.writer(open('all-action-by-score.csv', 'w'))
# f.writerow(['Name', 'Score', 'Link'])

pages = []
names_array = []
scores_array = []
links_array = []
all_array = []

for i in range(0, 1):  # model: range(0, (max # of pages))
    url = 'https://www.metacritic.com/browse/games/genre/metascore/action/all?view=detailed&page=' + str(i)
    pages.append(url)

for item in pages:
    page = requests.get(item, headers={'User-Agent': 'Mozilla/5.0'})
    soup = SOUP(page.text, 'html.parser')

    all_games_list = soup.find('table', class_='clamp-list')
    all_game_titles_list = all_games_list.find_all('h3')
    all_game_scores_list = all_games_list.find_all_next('div', class_='metascore_w large game positive')
    all_game_links_list = all_games_list.find_all('a', class_='title')

    # print(all_game_scores_list)

    for game_name in all_game_titles_list:
        names = game_name.contents[0].strip()
        names_array.append(names)
        # print(names)
    for game_score in all_game_scores_list:
        scores = game_score
        scores_array.append(scores)
        print(scores)
    for game_link in all_game_links_list:
        links = 'https://www.metacritic.com' + game_link.get('href')
        links_array.append(links)
        # print(links)



    # print(names_array)
    # print(scores_array)
    # print(links_array[0])
    # print(names_array[0]+' '+scores_array[0]+' '+links_array[0])
    # print(len(all_game_scores_list))




        # f.writerow([names, scores, links])
        # for i in names:
        # print(i)
        # print(names+' '+scores+' '+links)

'''
all_games_list = soup.find('table', class_='clamp-list')
all_game_titles_list = all_games_list.find_all('h3')
all_game_scores_list = all_games_list.find_all('div', class_='metascore_w large game positive')
all_game_links_list = all_games_list.find_all('a', class_='title')


for game_name in all_game_titles_list:
    names = game_name.contents[0]
    # print(names)
    # print(game_name.prettify())

for game_score in all_game_scores_list:
    scores = game_score.contents[0]
    # print(scores)

for game_link in all_game_links_list:
    links = 'https://www.metacritic.com' + game_link.get('href')
    # print(links)
'''