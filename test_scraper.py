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

f = csv.writer(open('all-action-by-score.csv', 'w'))
# f.writerow(['Name', 'Score', 'Link'])

pages = []

for i in range(0, 2):
    url = 'https://www.metacritic.com/browse/games/genre/metascore/action/all?view=detailed&page=' + str(i)
    pages.append(url)

for item in pages:
    page = requests.get(item, headers={'User-Agent': 'Mozilla/5.0'})
    soup = SOUP(page.text, 'html.parser')

    all_games_list = soup.find('table', class_='clamp-list')
    all_game_titles_list = all_games_list.find_all('h3')
    all_game_scores_list = all_games_list.find_all('div', class_='metascore_w large game positive')
    all_game_links_list = all_games_list.find_all('a', class_='title')

    for game_name in all_game_titles_list:
        names = game_name.contents[0]
        for game_score in all_game_scores_list:
            scores = game_score.contents[0]
            for game_link in all_game_links_list:
                links = 'https://www.metacritic.com' + game_link.get('href')

                # f.writerow([names, scores, links])
                print(names+scores+links)


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
    print(links)
'''







