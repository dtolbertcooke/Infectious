from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from forms import *
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def getID(self):
        return self.id

    def getUsername(self):
        return self.username


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Infectious is a fantastic app'
bootstrap = Bootstrap(app)
moment = Moment(app)
login_manager = LoginManager(app)
login_manager.login_view = 'home'
db = mysql.connector.connect(user='doug', password='infectious1234', host='127.0.0.1', database='users')
c = db.cursor()


def get_title_from_index(index):
    return df[df.index == index]["title"].values[0]


def get_index_from_title(title):
    return df[df.title == title]["index"].values[0]


def get_homepage_from_index(index):
    return df[df.index == index]["homepage"].values[0]


def combine_features(row):
    return row['genres'] + " " + row['keywords'] + " " + row["cast"] + " " + row["director"]


@login_manager.user_loader
def load_user(id):
    c.execute("SELECT * FROM registration WHERE id = '%s'" % id)
    data = c.fetchall()

    for row in data:
        id, username, pass_hash = row[0], row[3], row[8]
        user = User(id, username, pass_hash)
    return user


df = pd.read_csv("data/movie_dataset.csv")


features = ['genres', 'keywords', 'cast', 'director']
for feature in features:
    df[feature] = df[feature].fillna('')
df["combined_features"] = df.apply(combine_features, axis=1)

cv = CountVectorizer()  # Convert a collection of text documents to a matrix of token counts
count_matrix = cv.fit_transform(df["combined_features"])
cosine_sim = cosine_similarity(count_matrix)

similar_movies_array = []
similar_movies_homepage_array = []


@app.errorhandler(404)
def page_not_found(e):
    title = "404 - page not found"
    return render_template('404.html', title=title), 404


@app.errorhandler(500)
def internal_server_error(e):
    title = "500 - internal server error"
    return render_template('500.html', title=title), 500


@app.route('/', methods=['GET', 'POST'])
def home():
    title = 'Infectious - A movie recommendation system'
    form = LoginForm()

    if current_user.is_authenticated:
        # user = current_user
        return redirect(('user_profile/%s' % current_user.username))

    if form.validate_on_submit():
        username = form.username.data
        c.execute("SELECT * FROM registration WHERE username = '%s'" % username)
        data = c.fetchall()

        for row in data:
            id, username, pass_hash = row[0], row[3], row[8]
            user = User(id, username, pass_hash)

            if user is None or not check_password_hash(user.password, form.password.data):
                flash('Invalid username or password', 'danger')
                return redirect(url_for('home'))
            else:
                login_user(user)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('home')
                return redirect(next_page)
                return redirect('user_profile/%s' % username)
    return render_template("home.html", form=form, title=title)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/user_profile/<username>')
@login_required
def profile(username):
    title = "%s" % username + "'s profile"
    c.execute("SELECT * FROM registration WHERE username = '%s'" % username)
    data = c.fetchall()

    for row in data:
        fName = row[1]
        lName = row[2]
        username = row[3]
        age = row[4]
        location = row[5]
        bio = row[6]
        fave_genres = row[7]

    return render_template("profile.html", title=title, fName=fName, lName=lName, username=username, age=age,
                           location=location, bio=bio, fave_genres=fave_genres)


@app.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    title = 'Results'
    movie1 = similar_movies_array[0]
    movie2 = similar_movies_array[1]
    movie3 = similar_movies_array[2]
    movie4 = similar_movies_array[3]
    movie5 = similar_movies_array[4]
    movie6 = similar_movies_array[5]

    homepage1 = similar_movies_homepage_array[0]
    homepage2 = similar_movies_homepage_array[1]
    homepage3 = similar_movies_homepage_array[2]
    homepage4 = similar_movies_homepage_array[3]
    homepage5 = similar_movies_homepage_array[4]
    homepage6 = similar_movies_homepage_array[5]
    return render_template("results.html", title=title, movie1=movie1, movie2=movie2, movie3=movie3, movie4=movie4,
                           movie5=movie5, movie6=movie6, homepage1=homepage1, homepage2=homepage2, homepage3=homepage3,
                           homepage4=homepage4, homepage5=homepage5, homepage6=homepage6)


@app.route('/register', methods=['GET', 'POST'])
def register():
    title = 'Register'
    form = RegistrationForm()

    if form.validate_on_submit():
        fName = form.fName.data
        lName = form.lName.data
        username = form.username.data
        age = form.age.data
        location = form.location.data
        bio = form.bio.data
        fave_genres = form.fave_genres.data
        password_hash = generate_password_hash(form.password.data)
        user = User(id=id, username=form.username.data, password=password_hash)

        c.execute('INSERT INTO registration(fName, lName, username, age, location, bio, fave_genres, password_hash) values("%s","%s","%s","%s","%s","%s","%s","%s")' % (fName, lName, username, age, location, bio, fave_genres, password_hash))

        db.commit()
        flash("You have successfully been registered")
        return redirect(url_for('home'))
    return render_template("register.html", form=form, title=title)


@app.route('/edit_profile/<username>', methods=['GET', 'POST'])
def edit_profile(username):
    title = 'Edit Profile'
    form = EditProfileForm()

    if form.validate_on_submit():
        fName = form.fName.data
        lName = form.lName.data
        age = form.age.data
        location = form.location.data
        bio = form.bio.data
        fave_genres = form.fave_genres.data

        c.execute('UPDATE registration SET fName = "%s", lName = "%s", age = "%s", location = "%s", bio = "%s", fave_genres = "%s" WHERE username = "%s"' % (fName, lName, age, location, bio, fave_genres, username))
        db.commit()
        flash('Your profile has been updated!')
        return redirect(url_for('home'))

    elif request.method == 'GET':
        c.execute('SELECT * FROM registration WHERE username = "%s"' % username)
        data = c.fetchall()

        for row in data:
            fName = row[1]
            lName = row[2]
            age = row[4]
            location = row[5]
            bio = row[6]
            fave_genres = row[7]
        form.fName.data = fName
        form.lName.data = lName
        form.age.data = age
        form.location.data = location
        form.bio.data = bio
        form.fave_genres.data = fave_genres

    return render_template("edit_profile.html", form=form, title=title)


@app.route('/recommendation', methods=['GET', 'POST'])
@login_required
def recommendation():
    title = 'Recommendation'
    form = MovieForm()

    if form.validate_on_submit():
        movie_user_likes = form.movieName.data
        movie_index = get_index_from_title(movie_user_likes)
        similar_movies = list(enumerate(cosine_sim[movie_index]))
        sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:]

        i = 0
        for element in sorted_similar_movies:
            similar_movies_array.append(get_title_from_index(element[0]))
            similar_movies_homepage_array.append(get_homepage_from_index(element[0]))
            i = i + 1
            if i >= 7:
                break

        return redirect(url_for('results'))
    return render_template("recommendation.html", form=form, title=title)


@app.route('/how_to')
def how_to():
    title = 'How To'
    return render_template('how_to.html', title=title)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
