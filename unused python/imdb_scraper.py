import requests
from bs4 import BeautifulSoup as SOUP
import csv

# how-to run:
#   change f name to appropriate name
#   change range in first for loop to number of titles
#   choose appropriate url

# f = csv.writer(open('all-sport-games-IMDb.csv', 'w'))
# f.writerow(['Game Name', 'IMDb Score', 'Genre(s)', 'Game URL'])
# f.writerow([])

# g = csv.writer(open('all-game-names.csv', 'w'))
# g.writerow(['Game Name'])
# g.writerow([])

pages = []
names_array = []
scores_array = []
links_array = []
genres_array = []

for i in range(1, 2, 50):
    # top games url
    # url = 'https://www.imdb.com/search/title/?title_type=video_game&sort=user_rating,desc&start='+str(i)+'&view=advanced'

    # top drama games url
    # url = 'https://www.imdb.com/search/title/?title_type=video_game&genres=drama&sort=user_rating,desc&start='+str(i)+'&explore=title_type,genres&view=advanced'

    # top thriller games url
    # url = 'https://www.imdb.com/search/title/?title_type=video_game&genres=thriller&sort=user_rating,desc&start='+str(i)+'&explore=title_type,genres&view=advanced'

    # top sport games url
    url = 'https://www.imdb.com/search/title/?title_type=video_game&genres=sport&sort=user_rating,desc&start='+str(i)+'&explore=title_type,genres&view=advanced'

    # top adventure games url
    # url = 'https://www.imdb.com/search/title/?title_type=video_game&genres=adventure&sort=user_rating,desc&start='+str(i)+'&explore=title_type,genres&view=advanced'

    # top mystery games url
    # url = 'https://www.imdb.com/search/title/?title_type=video_game&genres=mystery&sort=user_rating,desc&start='+str(i)+'&explore=title_type,genres&view=advanced'

    # top horror games url
    # url = 'https://www.imdb.com/search/title/?title_type=video_game&genres=horror&sort=user_rating,desc&start='+str(i)+'&explore=title_type,genres&view=advanced'

    # top comedy games url
    # url = 'https://www.imdb.com/search/title/?title_type=video_game&genres=comedy&sort=user_rating,desc&start='+str(i)+'&explore=title_type,genres&view=advanced'

    pages.append(url)

for item in pages:
    # added headers to 'webpage' variable bc webpage security returned 403 error
    page = requests.get(item, headers={'User-Agent': 'Mozilla/5.0'})
    soup = SOUP(page.text, 'html.parser')

    all_game_titles_list = soup.find_all('h3', class_='lister-item-header')
    all_game_scores_list = soup.find_all('div', class_='inline-block ratings-imdb-rating')
    all_game_links_list = soup.find_all('h3', class_='lister-item-header')
    all_game_genres_list = soup.find_all('div', class_='lister-item-content')

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
    for all_tags in all_game_genres_list:
        for game_genre in all_tags.find_all('span', class_='genre'):
            genres = game_genre.contents[0].strip()
            genres_array.append(genres)
            # print(genres)
    for all_tags in all_game_links_list:
        # print(len(all_tags))
        for game_link in all_tags.find_all('a'):
            links = 'https://www.imdb.com' + game_link.get('href')
            links_array.append(links)
            # print(links)

    # for game name, score, genre and link
    # FIX THIS: for some reason, games are repeated throughout the loop
    for i, j, k, l in zip(range(len(names_array)), range(len(scores_array)), range(len(genres_array)), range(len(links_array))):
        print('%s ' % names_array[i], '%s ' % scores_array[j], '%s ' % genres_array[k], '%s ' % links_array[l])
        # f.writerow([names_array[i], scores_array[j], genres_array[k], links_array[l]])

    # for just game name
    # for x in range(len(names_array)):
    #     print(names_array[x])
    #     g.writerow([names_array[x]])

