from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, FileField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo


# Форма обратной связи
class FeedbackForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Тема', validators=[DataRequired(), Length(min=3, max=200)])
    message = TextAreaField('Сообщение', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Отправить')


# Форма регистрации
class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Роль', choices=[('student', 'Студент'), ('teacher', 'Преподаватель')])
    submit = SubmitField('Зарегистрироваться')


# Форма входа
class LoginForm(FlaskForm):
    username = StringField('Логин или Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


# Форма редактирования профиля студента
class StudentProfileForm(FlaskForm):
    full_name = StringField('ФИО', validators=[DataRequired(), Length(min=2, max=150)])
    group_name = StringField('Группа', validators=[DataRequired(), Length(min=2, max=50)])
    course = StringField('Курс', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[Optional()])
    telegram = StringField('Telegram', validators=[Optional()])
    bio = TextAreaField('О себе', validators=[Optional()])
    avatar = FileField('Фото профиля')
    submit = SubmitField('Сохранить изменения')


# Форма редактирования профиля преподавателя
class TeacherProfileForm(FlaskForm):
    full_name = StringField('ФИО', validators=[DataRequired(), Length(min=2, max=150)])
    department = StringField('Кафедра', validators=[DataRequired(), Length(min=2, max=100)])
    position = StringField('Должность', validators=[Optional(), Length(max=100)])
    degree = StringField('Учёная степень', validators=[Optional(), Length(max=100)])
    phone = StringField('Телефон', validators=[Optional(), Length(max=20)])
    bio = TextAreaField('О себе', validators=[Optional()])
    avatar = FileField('Фото профиля')
    submit = SubmitField('Сохранить изменения')


# Форма загрузки работы
class WorkUploadForm(FlaskForm):
    title = StringField('Название работы', validators=[DataRequired(), Length(min=3, max=200)])
    discipline_id = SelectField('Дисциплина', choices=[], coerce=int, validators=[DataRequired()])
    file = FileField('Файл (PDF, DOCX, XLSX)', validators=[DataRequired()])
    submit = SubmitField('Загрузить')


# Форма загрузки документа
class DocumentUploadForm(FlaskForm):
    title = StringField('Название документа', validators=[DataRequired(), Length(min=3, max=200)])
    file = FileField('Файл', validators=[DataRequired()])
    submit = SubmitField('Загрузить')


# Форма смены пароля
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Текущий пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Сменить пароль')


# Форма сообщений по работам
class WorkMessageForm(FlaskForm):
    message = TextAreaField('Сообщение', validators=[DataRequired(), Length(min=1, max=1000)])
    file = FileField('Файл с правками')
    submit = SubmitField('Отправить')

    class SiteSettingsForm(FlaskForm):
        site_title = StringField('Название сайта', validators=[Optional()])
        site_description = StringField('Описание сайта', validators=[Optional()])
        email = StringField('Email', validators=[Optional(), Email()])
        phone = StringField('Телефон', validators=[Optional()])
        address = StringField('Адрес', validators=[Optional()])
        work_hours = StringField('Часы работы', validators=[Optional()])
        vk_url = StringField('ВКонтакте', validators=[Optional()])
        telegram_url = StringField('Telegram', validators=[Optional()])
        primary_color = StringField('Основной цвет', validators=[Optional()])
        secondary_color = StringField('Вторичный цвет', validators=[Optional()])
        accent_color = StringField('Акцентный цвет', validators=[Optional()])
        logo = FileField('Логотип')
        about_text = TextAreaField('Текст о кафедре', validators=[Optional()])
        submit = SubmitField('Сохранить настройки')

    class AdminProfileForm(FlaskForm):
        username = StringField('Логин', validators=[DataRequired(), Length(min=3, max=80)])
        email = StringField('Email', validators=[DataRequired(), Email()])
        password = PasswordField('Новый пароль (оставьте пустым, чтобы не менять)')
        confirm_password = PasswordField('Подтвердите пароль', validators=[EqualTo('password')])
        submit = SubmitField('Сохранить профиль')