from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, Email, Optional

class StudentProfileForm(FlaskForm):
    full_name = StringField('ФИО', validators=[DataRequired(), Length(min=2, max=150)])
    group_name = StringField('Группа', validators=[DataRequired(), Length(min=2, max=50)])
    course = StringField('Курс', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[Optional()])
    telegram = StringField('Telegram', validators=[Optional()])
    bio = TextAreaField('О себе', validators=[Optional()])
    avatar = FileField('Фото профиля')
    submit = SubmitField('Сохранить изменения')