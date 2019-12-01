from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length


class EmotionForm(FlaskForm):
    emotion1 = SelectField('', choices=[(1, 'Select an emotion...'), ('Fear', 'Fear'),
                                   ('Anger', 'Anger'), ('Sadness', 'Sadness'),
                                   ('Joy', 'Joy'), ('Surprise', 'Surprise'),
                                   ('Trust', 'Trust'), ('Anticipation', 'Anticipation')],
                                    default=1)
    emotion2 = SelectField('', choices=[(1, 'Select an emotion...'), ('Fear', 'Fear'),
                                   ('Anger', 'Anger'), ('Sadness', 'Sadness'),
                                   ('Joy', 'Joy'), ('Surprise', 'Surprise'),
                                   ('Trust', 'Trust'), ('Anticipation', 'Anticipation')],
                                    default=1)
    emotion3 = SelectField('', choices=[(1, 'Select an emotion...'), ('Fear', 'Fear'),
                                   ('Anger', 'Anger'), ('Sadness', 'Sadness'),
                                   ('Joy', 'Joy'), ('Surprise', 'Surprise'),
                                   ('Trust', 'Trust'), ('Anticipation', 'Anticipation')],
                                    default=1)
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('', render_kw={"placeholder": "Username"},
                           validators=[DataRequired(), Length(min=3, max=20)])
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
