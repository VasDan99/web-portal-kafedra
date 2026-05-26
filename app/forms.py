from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class FeedbackForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Тема', validators=[DataRequired(), Length(min=3, max=200)])
    message = TextAreaField('Сообщение', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Отправить')