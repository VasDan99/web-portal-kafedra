from flask import render_template
from app.main import bp

@bp.route('/')
def index():
    breadcrumb_title = None
    return render_template('index.html', breadcrumb_title=breadcrumb_title)

@bp.route('/about')
def about():
    breadcrumb_title = 'О факультете ИТ'
    return render_template('about.html', breadcrumb_title=breadcrumb_title)

@bp.route('/history')
def history():
    breadcrumb_title = 'История факультета'
    return render_template('history.html', breadcrumb_title=breadcrumb_title)

@bp.route('/mission')
def mission():
    breadcrumb_title = 'Миссия и цели'
    return render_template('mission.html', breadcrumb_title=breadcrumb_title)

@bp.route('/team')
def team():
    breadcrumb_title = 'Команда факультета'
    return render_template('team.html', breadcrumb_title=breadcrumb_title)

@bp.route('/departments')
def departments():
    breadcrumb_title = 'Кафедры факультета'
    return render_template('departments.html', breadcrumb_title=breadcrumb_title)

@bp.route('/teachers')
def teachers():
    breadcrumb_title = 'Преподаватели'
    return render_template('teachers.html', breadcrumb_title=breadcrumb_title)

@bp.route('/disciplines')
def disciplines():
    breadcrumb_title = 'Дисциплины'
    return render_template('disciplines.html', breadcrumb_title=breadcrumb_title)

@bp.route('/discipline/<int:disc_id>')
def discipline_detail(disc_id):
    disciplines_data = {
        1: {'name': 'Программирование', 'description': 'Изучение языков программирования, алгоритмов и структур данных.'},
        2: {'name': 'Базы данных', 'description': 'Проектирование, разработка и администрирование баз данных.'},
        3: {'name': 'Web-технологии', 'description': 'Разработка веб-приложений на современных фреймворках.'},
        4: {'name': 'Искусственный интеллект', 'description': 'Нейронные сети, машинное обучение и анализ данных.'}
    }
    disc = disciplines_data.get(disc_id, {'name': 'Дисциплина', 'description': 'Описание'})
    breadcrumb_title = disc['name']
    return render_template('discipline_detail.html', breadcrumb_title=breadcrumb_title, discipline=disc)

@bp.route('/schedule')
def schedule():
    breadcrumb_title = 'Расписание занятий'
    return render_template('schedule.html', breadcrumb_title=breadcrumb_title)

@bp.route('/science-works')
def science_works():
    breadcrumb_title = 'Научные работы'
    return render_template('science_works.html', breadcrumb_title=breadcrumb_title)

@bp.route('/contacts')
def contacts():
    breadcrumb_title = 'Контакты'
    return render_template('contacts.html', breadcrumb_title=breadcrumb_title)

@bp.route('/feedback')
def feedback():
    breadcrumb_title = 'Обратная связь'
    return render_template('feedback.html', breadcrumb_title=breadcrumb_title)