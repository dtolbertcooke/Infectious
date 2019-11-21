from urllib.request import Request, urlopen
import ssl
from bs4 import BeautifulSoup
import re
import time
import random

TAG_RE = re.compile(r'<[^>]+>')


def remove_tags(text):
    return TAG_RE.sub('', text)


def pre_processing_data(my_URL):
    context = ssl._create_unverified_context()
    req = Request(str(my_URL), headers={'User-Agent': 'Mozilla/5.0'})
    get_SER = urlopen(req, context=context).read()

    soup = BeautifulSoup(get_SER, features="html.parser")
    find_all_clamp_summary_wrap = soup.find_all('h3')

    find_all_meta_score = soup.find_all("div", class_="metascore_w large game positive")

    a = []
    b = []
    c = []
    f = []
    g = []

    num = 29
    for index, value in enumerate(find_all_clamp_summary_wrap):
        a.append(str(value))
        if num == index:
            break

    for x in a:
        aa = remove_tags(x)
        b.append(aa)

    the_n_sing = [x.strip(' ') for x in b]

    for x in the_n_sing:
        j = x.replace(' ', '')
        c.append(j)

    d = map(lambda s: s.strip(), c)

    e = list(d)

    for x in find_all_meta_score:
        f.append(str(x))

    indexx = 0
    for index, value in enumerate(f):
        if index % 2:
            indexx += 1
            dfdf = remove_tags(value)
            g.append(dfdf)
        else:
            pass

    return e, g


the_URL = 'https://www.metacritic.com/browse/games/genre/metascore/action/ps4?view=detailed'

num_count = 0
for x in range(29): #change range value based on number of pages
    game_name, game_score = pre_processing_data(the_URL + '&page='+str(x))
    with open('data_file.txt', 'a') as filehandle:
        for g_name, m_score in zip(game_name, game_score):
            num_count += 1
            filehandle.write('%s ' % num_count + '%s ' % g_name + '%s\n' % m_score)

    randooom_num = random.randint(10, 25)*5,
    wait_time = int(randooom_num[0])
    time.sleep(wait_time)
    print('Page number', x, 'Wait TIme', wait_time)

filehandle.close()
