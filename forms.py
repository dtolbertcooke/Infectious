from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length


class EmotionForm(FlaskForm):
    emotion1 = StringField('', render_kw={"placeholder": "Enter an emotion..."})
    emotion2 = StringField('', render_kw={"placeholder": "Enter an emotion..."})
    emotion3 = StringField('', render_kw={"placeholder": "Enter an emotion..."})
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('', render_kw={"placeholder": "Username"}, validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('', render_kw={"placeholder": "Password"}, validators=[DataRequired(), Length(min=3, max=20)])
    login = SubmitField('Login')


class RegisterForm(FlaskForm):
    fName = StringField('', render_kw={"placeholder": "First name"}, validators=[DataRequired(), Length(min=3, max=20)])
    lName = StringField('', render_kw={"placeholder": "Last name"}, validators=[DataRequired(), Length(min=3, max=20)])
    username = StringField('', render_kw={"placeholder": "Username"}, validators=[DataRequired(), Length(min=6, max=35)])
    submit = SubmitField('Submit')
