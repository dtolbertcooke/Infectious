from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, SelectField


class EmotionForm(FlaskForm):
    emotion1 = StringField('', render_kw={"placeholder": "Enter an emotion..."})
    emotion2 = StringField('', render_kw={"placeholder": "Enter an emotion..."})
    emotion3 = StringField('', render_kw={"placeholder": "Enter an emotion..."})
    submit = SubmitField('Submit')