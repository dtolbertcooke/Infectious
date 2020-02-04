from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from forms import *
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pymysql
import sys
from bs4 import BeautifulSoup as SOUP
import re
import requests as HTTP
import numpy as np

# from flask_user import roles_required


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Infectious is a fantastic app'
# app.db = None
# app.db = pymysql.connect('127.0.0.1', 'root', 'infectious', 'infectious')
# c = app.db.cursor()
bootstrap = Bootstrap(app)
moment = Moment(app)


def get_name_from_game_id(game_id):
    return df[df.game_id == game_id]["name"].values[0]

# def get_name_from_game_id(game_id):
#     return c.execute('SELECT name FROM mytable WHERE game_id = %s;' % game_id)

def get_game_id_from_name(name):
    return df[df.name == name]["game_id"].values[0]

# def get_game_id_from_name(name):
#     return c.execute('SELECT game_id FROM mytable WHERE name = %s;' % name)

def combine_features(row):
    return row['categories'] + " " + row['genres'] + " " + row["steamspy_tags"]


# df = pd.read_csv("data/steam_games_dataset.csv")
# print(df.columns)
df = pd.read_csv("data/small_dataset.csv")


# def get_categories():
#     # app.db = pymysql.connect('127.0.0.1', 'root', 'infectious', 'infectious')
#     # c = app.db.cursor()
#     c.execute('SELECT categories FROM mytable;')
#     categories_data = c.fetchall()
#     app.db.commit()
#     c.close()
#     return categories_data
#
#
# def get_genres():
#     c = app.db.cursor()
#     query = "SELECT genres FROM mytable;"
#     c.execute(query)
#     genres_data = c.fetchall()
#     app.db.commit()
#     c.close()
#     return genres_data
#
#
# def get_steamspy_tags():
#     query = "SELECT genres FROM mytable;"
#     c = app.db.cursor()
#     c.execute(query)
#     steamspy_data = c.fetchall()
#     app.db.commit()
#     c.close()
#     return steamspy_data
#
#
# def combine():
#     categories = get_categories()
#     genres = get_genres()
#     steamspy_id = get_steamspy_tags()
#     combined = categories + genres + steamspy_id
#     return combined


# print(combine())

# categories = get_categories()
# genres = get_genres()
# steamspy_id = get_steamspy_tags()

# print(categories[0], genres[0], steamspy_id[0])

features = ['categories', 'genres', 'steamspy_tags']
df["combined_features"] = df.apply(combine_features, axis=1)
cv = CountVectorizer()  # Convert a collection of text documents to a matrix of token counts
count_matrix = cv.fit_transform(df["combined_features"])
# count_matrix = cv.fit_transform(combine())
# print(type(df["combined_features"])) // --> <class 'pandas.core.series.Series'>
cosine_sim = cosine_similarity(count_matrix)
# game_user_likes = "Left 4 Dead"

similar_games_array = []


@app.route('/', methods=['GET', 'POST'])
def home():
    title = 'Infectious - A video game recommendation system'
    form = EmotionForm()

    if form.validate_on_submit():
        game_user_likes = form.gameName.data
        game_index = get_game_id_from_name(game_user_likes)
        similar_games = list(enumerate(cosine_sim[game_index]))
        sorted_similar_games = sorted(similar_games, key=lambda x: x[1], reverse=True)

        i = 0
        for element in sorted_similar_games:
            similar_games_array.append(get_name_from_game_id(element[0]))
            # print(similar_games_array[i])
            sim_games = get_name_from_game_id(element[0])
            similar_games_array.append(sim_games)
            # print(sim_games)
            i = i + 1
            if i >= 7:
                break
        # print(similar_games_array)
        # for i in similar_games_array:
        #     print(i)

        return redirect(url_for('results'))
    return render_template("home.html", form=form, title=title)


@app.route('/results', methods=['GET', 'POST'])
def results():
    title = 'Results'
    game1 = similar_games_array[1]
    game2 = similar_games_array[2]
    game3 = similar_games_array[3]
    game4 = similar_games_array[4]
    game5 = similar_games_array[5]
    game6 = similar_games_array[6]
    return render_template("results.html", title=title, game1=game1, game2=game2, game3=game3, game4=game4, game5=game5,
                           game6=game6)


@app.route('/register', methods=['GET', 'POST'])
def signup():
    title = 'Register'
    form = RegisterForm()
    return render_template("register.html", form=form, title=title)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Login'
    form = LoginForm()
    return render_template("login.html", form=form, title=title)


@app.route('/test')
def test_page():
    return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
