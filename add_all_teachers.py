from app import create_app, db
from app.models import Teacher, User

app = create_app()

teachers_data = [
    {'full_name': 'Атаева Ольга Муратовна', 'department': 'Кафедра ИС', 'position': 'Старший научный сотрудник, доцент',
     'degree': 'Кандидат технических наук', 'username': 'ataeva', 'password': 'ataeva123'},
    {'full_name': 'Блощук Андрей Алексеевич', 'department': 'Кафедра ИС', 'position': 'Доцент кафедры',
     'degree': 'Кандидат технических наук', 'username': 'bloschuk', 'password': 'bloschuk123'},
    {'full_name': 'Имани Ханум Курбанкадыевна', 'department': 'Кафедра ИС', 'position': 'Старший преподаватель',
     'degree': '', 'username': 'imani', 'password': 'imani123'},
    {'full_name': 'Киселев Федор Владимирович', 'department': 'Кафедра ИС', 'position': 'Старший преподаватель',
     'degree': '', 'username': 'kiselev', 'password': 'kiselev123'},
    {'full_name': 'Королькова Ирина Анатольевна', 'department': 'Кафедра ИС',
     'position': 'Руководитель образовательной программы, старший преподаватель', 'degree': '', 'username': 'korolkova',
     'password': 'korolkova123'},
    {'full_name': 'Преображенский Максим Владимирович', 'department': 'Кафедра ИС', 'position': 'Старший преподаватель',
     'degree': '', 'username': 'preobrazhensky', 'password': 'preobrazhensky123'},
    {'full_name': 'Пузицкий Михаил Леонидович', 'department': 'Кафедра ИС', 'position': 'Преподаватель', 'degree': '',
     'username': 'puzitsky', 'password': 'puzitsky123'},
    {'full_name': 'Стряпунина Нэля Ильинична', 'department': 'Кафедра ИС', 'position': 'Старший преподаватель',
     'degree': '', 'username': 'stryapunina', 'password': 'stryapunina123'},
    {'full_name': 'Сурина Елена Евгеньевна', 'department': 'Кафедра ИС', 'position': 'Заведующий кафедрой, доцент',
     'degree': 'Кандидат экономических наук', 'username': 'surina', 'password': 'surina123'},
]

with app.app_context():
    for t in teachers_data:
        # Проверяем, есть ли пользователь
        user = User.query.filter_by(username=t['username']).first()
        if not user:
            user = User(
                username=t['username'],
                email=f"{t['username']}@vitte.ru",
                role='teacher'
            )
            user.set_password(t['password'])
            db.session.add(user)
            db.session.flush()

            teacher = Teacher(
                user_id=user.id,
                full_name=t['full_name'],
                department=t['department'],
                position=t['position'],
                degree=t['degree']
            )
            db.session.add(teacher)
            print(f'Добавлен: {t["full_name"]} (логин: {t["username"]}, пароль: {t["password"]})')
        else:
            print(f'Уже существует: {t["full_name"]}')

    db.session.commit()
    print('\nГотово! Все преподаватели добавлены.')
    print('\nЛогины и пароли для входа:')
    for t in teachers_data:
        print(f'  {t["username"]} / {t["password"]}')