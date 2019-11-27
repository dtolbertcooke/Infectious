import requests
from bs4 import BeautifulSoup as SOUP
import csv

f = csv.writer(open('all-action-by-score.csv', 'w'))
f.writerow(['Game Name', 'Metacritic Score', 'Game URL'])
f.writerow([])

pages = []
names_array = []
scores_array = []
links_array = []

for i in range(0, 332):  # model: range(0, (max # of pages))
    url = 'https://www.metacritic.com/browse/games/genre/metascore/action/all?view=detailed&page=' + str(i)
    pages.append(url)

for item in pages:
    # added headers to 'webpage' variable bc webpage security returned 403 error
    page = requests.get(item, headers={'User-Agent': 'Mozilla/5.0'})
    soup = SOUP(page.text, 'html.parser')

    all_games_list = soup.find('table', class_='clamp-list')
    all_game_titles_list = all_games_list.find_all('h3')
    all_game_scores_list = all_games_list.find_all_next('div', class_='metascore_w large game positive')
    all_game_links_list = all_games_list.find_all('a', class_='title')

    for game_name in all_game_titles_list:
        names = game_name.contents[0].strip()
        names_array.append(names)
        # print(game_name.prettify())
        # print(names)
    for index, game_score in enumerate(all_game_scores_list):
        if index % 2:
            scores = game_score.contents[0]
            scores_array.append(scores)
            # print(scores)
    for game_link in all_game_links_list:
        links = 'https://www.metacritic.com' + game_link.get('href')
        links_array.append(links)
        # print(links)

    for i, j, k in zip(range(len(names_array)), range(len(scores_array)), range(len(links_array))):
        # print('%s ' % names_array[i], '%s ' % scores_array[j], '%s ' % links_array[k])
        f.writerow([names_array[i], scores_array[j], links_array[k]])
