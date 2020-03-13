import mysql.connector
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, AnyOf, ValidationError
from wtforms.widgets.html5 import NumberInput

db = mysql.connector.connect(user='doug', password='infectious1234', host='127.0.0.1', database='users')
c = db.cursor()


class MovieForm(FlaskForm):
    movieName = StringField('', render_kw={"placeholder": "Movie name"},
                            validators=[DataRequired(), Length(min=3, max=20)])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('', render_kw={"placeholder": "Username"},
                           validators=[DataRequired(), Length(min=3, max=35)])
    password = PasswordField('', render_kw={"placeholder": "Password"},
                             validators=[DataRequired(), Length(min=3, max=20)])
    login = SubmitField('Login')


class RegistrationForm(FlaskForm):
    fName = StringField('', render_kw={"placeholder": "First name"},
                        validators=[DataRequired(), Length(min=3, max=20)])
    lName = StringField('', render_kw={"placeholder": "Last name"},
                        validators=[DataRequired(), Length(min=3, max=20)])
    username = StringField('', render_kw={"placeholder": "Username"},
                           validators=[DataRequired(), Length(min=6, max=35)])
    age = IntegerField('', render_kw={"placeholder": "Age"},
                       validators=[DataRequired()], widget=NumberInput())
    location = StringField('', render_kw={"placeholder": "Location"})
    bio = TextAreaField('', render_kw={"placeholder": "Biography"},
                        validators=[Length(min=0, max=500)])
    fave_genres = StringField('', render_kw={"placeholder": "Favorite genres"})
    password = PasswordField('', render_kw={"placeholder": "Password"},
                             validators=[DataRequired(), Length(min=6),
                                         EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('', render_kw={"placeholder": "Repeat Password"},
                            validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        c.execute("SELECT username FROM registration WHERE username = '%s'" % username)
        msg = c.fetchone()
        if msg:
            raise ValidationError('Please use a different username.')


class EditProfileForm(FlaskForm):
    fName = StringField('', render_kw={"placeholder": "First name"},
                        validators=[DataRequired(), Length(min=3, max=20)])
    lName = StringField('', render_kw={"placeholder": "Last name"},
                        validators=[DataRequired(), Length(min=3, max=20)])
    age = IntegerField('', render_kw={"placeholder": "Age"},
                       validators=[DataRequired()], widget=NumberInput())
    location = StringField('', render_kw={"placeholder": "Location"})
    bio = TextAreaField('', render_kw={"placeholder": "Biography"},
                        validators=[Length(min=0, max=500)])
    fave_genres = StringField('', render_kw={"placeholder": "Favorite genres"})
    submit = SubmitField('Submit')
