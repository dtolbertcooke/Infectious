from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from forms import *
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, SelectField
from wtforms.validators import DataRequired, NumberRange
from bs4 import BeautifulSoup as SOUP
import re
import requests as HTTP

'''
import pymysql
from flask_user import roles_required   # we will have three roles; admin, intern, sponsor
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Infectious is a fantastic app'

bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    title = 'Infectious - A video game recommendation system based on emotion'
    form = EmotionForm()
    return render_template("home.html", form=form, title=title)


@app.route('/results', methods=['GET', 'POST'])
def results():
    title = 'Results'
    return render_template("results.html", title=title)


@app.route('/test')
def test_page():
    return render_template('test.html')


def main(emotion_param):
    # IMDb Url for Drama genre of
    # movie against emotion Sad
    if (emotion_param == "Sad"):
        urlhere = 'http://www.imdb.com/search/title?genres=drama&title_type=feature&sort=moviemeter, asc'

    # IMDb Url for Musical genre of
    # movie against emotion Disgust
    elif (emotion_param == "Disgust"):
        urlhere = 'http://www.imdb.com/search/title?genres=musical&title_type=feature&sort=moviemeter, asc'

    # IMDb Url for Family genre of
    # movie against emotion Anger
    elif (emotion_param == "Anger"):
        urlhere = 'http://www.imdb.com/search/title?genres=family&title_type=feature&sort=moviemeter, asc'

    # IMDb Url for Thriller genre of
    # movie against emotion Anticipation
    elif (emotion_param == "Anticipation"):
        urlhere = 'http://www.imdb.com/search/title?genres=thriller&title_type=feature&sort=moviemeter, asc'

    # IMDb Url for Sport genre of
    # movie against emotion Fear
    elif (emotion_param == "Fear"):
        urlhere = 'http://www.imdb.com/search/title?genres=sport&title_type=feature&sort=moviemeter, asc'

    # IMDb Url for Thriller genre of
    # movie against emotion Enjoyment
    elif (emotion_param == "Enjoyment"):
        urlhere = 'http://www.imdb.com/search/title?genres=thriller&title_type=feature&sort=moviemeter, asc'

    # IMDb Url for Western genre of
    # movie against emotion Trust
    elif (emotion_param == "Trust"):
        urlhere = 'http://www.imdb.com/search/title?genres=western&title_type=feature&sort=moviemeter, asc'

    # IMDb Url for Film_noir genre of
    # movie against emotion Surprise
    elif (emotion_param == "Surprise"):
        urlhere = 'http://www.imdb.com/search/title?genres=film_noir&title_type=feature&sort=moviemeter, asc'

    # HTTP request to get the data of
    # the whole page
    response = HTTP.get(urlhere)
    data = response.text

    # Parsing the data using
    # BeautifulSoup
    soup = SOUP(data, "lxml")

    # Extract movie titles from the
    # data using regex
    title = soup.find_all("a", attrs={"href": re.compile(r'\/title\/tt+\d*\/')})
    return title


if __name__ == '__main__':
    app.run(debug=True, port=5000)
