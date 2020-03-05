from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from forms import *
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import mysql.connector
from mysql.connector import errorcode
from werkzeug.security import generate_password_hash, check_password_hash
# import pymysql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Infectious is a fantastic app'
bootstrap = Bootstrap(app)
moment = Moment(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# db = pymysql.connect(host='127.0.0.1', user='root', password='capitalD95', db='Infectious')
db = mysql.connector.connect(user='doug', password='infectious1234', host='127.0.0.1', database='users')
c = db.cursor()


def get_title_from_index(index):
    return df[df.index == index]["title"].values[0]


def get_index_from_title(title):
    return df[df.title == title]["index"].values[0]


def combine_features(row):
    return row['genres'] + " " + row['keywords'] + " " + row["cast"] + " " + row["director"]


df = pd.read_csv("data/movie_dataset.csv")
# print(df.columns)


features = ['genres', 'keywords', 'cast', 'director']
for feature in features:
    df[feature] = df[feature].fillna('')
df["combined_features"] = df.apply(combine_features, axis=1)

cv = CountVectorizer()  # Convert a collection of text documents to a matrix of token counts
count_matrix = cv.fit_transform(df["combined_features"])
cosine_sim = cosine_similarity(count_matrix)
# movie_user_likes = "Avatar"

similar_movies_array = []


@app.errorhandler(404)
def page_not_found(e):
    title = "404 - page not found"
    return render_template('404.html', title=title), 404


@app.errorhandler(500)
def internal_server_error(e):
    title = "505 - internal server error"
    return render_template('500.html', title=title), 500


@app.route('/', methods=['GET', 'POST'])
def home():
    title = 'Infectious - A video game recommendation system'
    form = MovieForm()

    if form.validate_on_submit():
        movie_user_likes = form.movieName.data
        movie_index = get_index_from_title(movie_user_likes)
        similar_movies = list(enumerate(cosine_sim[movie_index]))
        sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:]

        i = 0
        for element in sorted_similar_movies:
            similar_movies_array.append(get_title_from_index(element[0]))
            i = i + 1
            if i >= 7:
                break

        return redirect(url_for('results'))
    return render_template("home.html", form=form, title=title)


@app.route('/results', methods=['GET', 'POST'])
def results():
    title = 'Results'
    movie1 = similar_movies_array[0]
    movie2 = similar_movies_array[1]
    movie3 = similar_movies_array[2]
    movie4 = similar_movies_array[3]
    movie5 = similar_movies_array[4]
    movie6 = similar_movies_array[5]
    return render_template("results.html", title=title, movie1=movie1, movie2=movie2, movie3=movie3, movie4=movie4,
                           movie5=movie5, movie6=movie6)


@app.route('/register', methods=['GET', 'POST'])
def register():
    title = 'Register'
    form = RegistrationForm()

    if form.validate_on_submit():
        fName = form.fName.data
        lName = form.lName.data
        username = form.username.data
        password_hash = generate_password_hash(form.password.data)

        c.execute('INSERT INTO registration values("%s","%s","%s","%s")' % (
        fName, lName, username, password_hash))

        db.commit()
        return redirect(url_for('home'))
    return render_template("register.html", form=form, title=title)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Login'
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password_hash = generate_password_hash(form.password.data)

        # password_hash = generate_password_hash(password)
        # check_password_hash(password_hash, password)
    return render_template("login.html", form=form, title=title)


@app.route('/test')
def test_page():
    return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
