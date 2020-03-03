from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, AnyOf


# Fix validators. They're supposed to make it so 1 value is acceptable. Currently, it requires all 3.
# class EmotionForm(FlaskForm):
class MovieForm(FlaskForm):
    movieName = StringField('', render_kw={"placeholder": "Movie name"},
                           validators=[DataRequired(), Length(min=3, max=20)])

    # emotion1 = SelectField('', choices=[(1, 'Select an emotion...'), ('Fear', 'Fear'),
    #                                     ('Anger', 'Anger'), ('Sadness', 'Sadness'),
    #                                     ('Joy', 'Joy'), ('Surprise', 'Surprise'),
    #                                     ('Trust', 'Trust'), ('Anticipation', 'Anticipation')],
    #                        default=1, validators=[DataRequired()])
    # emotion2 = SelectField('', choices=[(1, 'Select an emotion...'), ('Fear', 'Fear'),
    #                                     ('Anger', 'Anger'), ('Sadness', 'Sadness'),
    #                                     ('Joy', 'Joy'), ('Surprise', 'Surprise'),
    #                                     ('Trust', 'Trust'), ('Anticipation', 'Anticipation')],
    #                        default=1, validators=[
    #         AnyOf(['Select an emotion...', 'Fear', 'Anger', 'Sadness', 'Joy', 'Surprise', 'Trust', 'Anticipation'])])
    # emotion3 = SelectField('', choices=[(1, 'Select an emotion...'), ('Fear', 'Fear'),
    #                                     ('Anger', 'Anger'), ('Sadness', 'Sadness'),
    #                                     ('Joy', 'Joy'), ('Surprise', 'Surprise'),
    #                                     ('Trust', 'Trust'), ('Anticipation', 'Anticipation')],
    #                        default=1, validators=[
    #         AnyOf(['Select an emotion...', 'Fear', 'Anger', 'Sadness', 'Joy', 'Surprise', 'Trust', 'Anticipation'])])

    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('', render_kw={"placeholder": "Username"},
                           validators=[DataRequired(), Length(min=3, max=35)])
    password = PasswordField('', render_kw={"placeholder": "Password"},
                             validators=[DataRequired(), Length(min=3, max=20)])
    login = SubmitField('Login')


class RegisterForm(FlaskForm):
    fName = StringField('', render_kw={"placeholder": "First name"},
                        validators=[DataRequired(), Length(min=3, max=20)])
    lName = StringField('', render_kw={"placeholder": "Last name"},
                        validators=[DataRequired(), Length(min=3, max=20)])
    username = StringField('', render_kw={"placeholder": "Username"},
                           validators=[DataRequired(), Length(min=6, max=35)])
    submit = SubmitField('Submit')
