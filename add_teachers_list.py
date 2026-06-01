from app import create_app, db
from app.models import Teacher

app = create_app()

teachers_data = [
    {'full_name': 'Атаева Ольга Муратовна', 'department': 'Кафедра ИС', 'position': 'Старший научный сотрудник, доцент',
     'degree': 'Кандидат технических наук'},
    {'full_name': 'Блощук Андрей Алексеевич', 'department': 'Кафедра ИС', 'position': 'Доцент кафедры',
     'degree': 'Кандидат технических наук'},
    {'full_name': 'Имани Ханум Курбанкадыевна', 'department': 'Кафедра ИС', 'position': 'Старший преподаватель',
     'degree': ''},
    {'full_name': 'Киселев Федор Владимирович', 'department': 'Кафедра ИС', 'position': 'Старший преподаватель',
     'degree': ''},
    {'full_name': 'Королькова Ирина Анатольевна', 'department': 'Кафедра ИС',
     'position': 'Руководитель образовательной программы, старший преподаватель', 'degree': ''},
    {'full_name': 'Преображенский Максим Владимирович', 'department': 'Кафедра ИС', 'position': 'Старший преподаватель',
     'degree': ''},
    {'full_name': 'Пузицкий Михаил Леонидович', 'department': 'Кафедра ИС', 'position': 'Преподаватель', 'degree': ''},
    {'full_name': 'Стряпунина Нэля Ильинична', 'department': 'Кафедра ИС', 'position': 'Старший преподаватель',
     'degree': ''},
    {'full_name': 'Сурина Елена Евгеньевна', 'department': 'Кафедра ИС', 'position': 'Заведующий кафедрой, доцент',
     'degree': 'Кандидат экономических наук'}
]

with app.app_context():
    for t in teachers_data:
        existing = Teacher.query.filter_by(full_name=t['full_name']).first()
        if not existing:
            teacher = Teacher(
                full_name=t['full_name'],
                department=t['department'],
                position=t['position'],
                degree=t['degree']
            )
            db.session.add(teacher)
            print(f'Добавлен: {t["full_name"]}')
        else:
            print(f'Уже существует: {t["full_name"]}')

    db.session.commit()
    print('Готово! Преподаватели добавлены.')