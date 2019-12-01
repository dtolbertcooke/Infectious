import requests
from bs4 import BeautifulSoup as SOUP
import csv
import re

'''
Metacritic eventually disconnects me so I can't scrape EVERY page
but I can get a good amount of data before I'm disconnected
'''

# f = csv.writer(open('all-PS4-action-by-score.csv', 'w'))
# f.writerow(['Game Name', 'Metacritic Score', 'Game URL'])
# f.writerow([])

# g = csv.writer(open('all-game-names.csv', 'w'))
# g.writerow(['Game Name'])
# g.writerow([])

pages = []
names_array = []
scores_array = []
links_array = []

for i in range(1, 2, 50):
    # # top games url
    # url = 'https://www.imdb.com/search/title/?title_type=video_game&sort=user_rating,desc&start='+str(i)+'&view=advanced'
    # # top drama games url
    # url = 'https://www.imdb.com/search/title/?title_type=video_game&genres=drama&sort=user_rating,desc&start='+str(i)+'&explore=title_type,genres&view=advanced'
    # # top thriller games url
    # url = 'https://www.imdb.com/search/title/?title_type=video_game&genres=thriller&sort=user_rating,desc&start='+str(i)+'&explore=title_type,genres&view=advanced'
    # # top sport games url
    # url = 'https://www.imdb.com/search/title/?title_type=video_game&genres=sport&sort=user_rating,desc&start='+str(i)+'&explore=title_type,genres&view=advanced'
    # # top adventure games url
    # url = 'https://www.imdb.com/search/title/?title_type=video_game&genres=adventure&sort=user_rating,desc&start='+str(i)+'&explore=title_type,genres&view=advanced'
    # # top mystery games url
    # url = 'https://www.imdb.com/search/title/?title_type=video_game&genres=mystery&sort=user_rating,desc&start='+str(i)+'&explore=title_type,genres&view=advanced'
    # # top horror games url
    # url = 'https://www.imdb.com/search/title/?title_type=video_game&genres=horror&sort=user_rating,desc&start='+str(i)+'&explore=title_type,genres&view=advanced'
    # # top comedy games url
    url = 'https://www.imdb.com/search/title/?title_type=video_game&genres=comedy&sort=user_rating,desc&start='+str(i)+'&explore=title_type,genres&view=advanced'

    pages.append(url)

for item in pages:
    # added headers to 'webpage' variable bc webpage security returned 403 error
    page = requests.get(item, headers={'User-Agent': 'Mozilla/5.0'})
    soup = SOUP(page.text, 'html.parser')

    all_game_titles_list = soup.find_all('h3', class_='lister-item-header')
    all_game_scores_list = soup.find_all('div', class_='inline-block ratings-imdb-rating')
    all_game_links_list = soup.find_all('h3', class_='lister-item-header')
    all_game_genres_list = soup.find_all('span', class_='genre')

    for all_tags in all_game_titles_list:
        for game_name in all_tags.find_all('a'):
            names = game_name.text
            names_array.append(names)
            # print(game_name.prettify())
            # print(names)
    for all_tags in all_game_scores_list:
        for game_score in all_tags.find_all('strong'):
            scores = game_score.text
            scores_array.append(scores)
            # print(scores)
    for game_genre in all_game_genres_list:
        genres = game_genre.contents[0]
        print(genres)
    for all_tags in all_game_links_list:
        for game_link in all_tags.find_all('a'):
            links = 'https://www.imdb.com' + game_link.get('href')
            links_array.append(links)
            # print(links)

    # for game name, score and link
    #for i, j, k in zip(range(len(names_array)), range(len(scores_array)), range(len(links_array))):
        #print('%s ' % names_array[i], '%s ' % scores_array[j], '%s ' % links_array[k])
        # f.writerow([names_array[i], scores_array[j], links_array[k]])

    # for just game name
    # for x in range(len(names_array)):
    #     g.writerow([names_array[x]])

