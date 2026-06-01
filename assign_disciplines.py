from app import create_app, db
from app.models import Teacher, Discipline, User

app = create_app()

disciplines_teachers = [
    ('Программирование', 'kiselev'),
    ('Базы данных', 'korolkova'),
    ('Web-технологии', 'kiselev'),
    ('Искусственный интеллект', 'ataeva'),
    ('Компьютерные сети', 'bloschuk'),
    ('Офисные приложения', 'imani'),
    ('1С: Предприятие', 'stryapunina'),
    ('Управление IT проектами', 'bloschuk'),
    ('Алгоритмизация', 'kiselev'),
    ('Реляционные базы данных', 'korolkova'),
]

with app.app_context():
    for disc_name, username in disciplines_teachers:
        # Находим преподавателя по username
        user = User.query.filter_by(username=username).first()
        if user:
            teacher = Teacher.query.filter_by(user_id=user.id).first()
            discipline = Discipline.query.filter_by(name=disc_name).first()

            if teacher and discipline:
                discipline.teacher_id = teacher.id
                print(f'Дисциплина "{disc_name}" привязана к {teacher.full_name}')
            else:
                print(f'Не найдено: дисциплина "{disc_name}" или преподаватель {username}')
        else:
            print(f'Пользователь {username} не найден')

    db.session.commit()
    print('\nГотово! Дисциплины привязаны к преподавателям.')