from app import create_app, db
from app.models import User, Student
import random

app = create_app()

students_data = [
    {'username': 'belov_ivan', 'email': 'belov.ivan@student.ru', 'full_name': 'Белов Иван Андреевич', 'group': 'ИС-01',
     'course': 1, 'phone': '+7-915-123-45-01'},
    {'username': 'volkova_anna', 'email': 'volkova.anna@student.ru', 'full_name': 'Волкова Анна Сергеевна',
     'group': 'ИС-01', 'course': 1, 'phone': '+7-915-123-45-02'},
    {'username': 'morozov_dmitry', 'email': 'morozov.dmitry@student.ru', 'full_name': 'Морозов Дмитрий Алексеевич',
     'group': 'ИС-01', 'course': 1, 'phone': '+7-915-123-45-03'},
    {'username': 'sokolova_ekaterina', 'email': 'sokolova.ekaterina@student.ru',
     'full_name': 'Соколова Екатерина Владимировна', 'group': 'ИС-02', 'course': 2, 'phone': '+7-915-123-45-04'},
    {'username': 'kovalev_maxim', 'email': 'kovalev.maxim@student.ru', 'full_name': 'Ковалёв Максим Денисович',
     'group': 'ИС-02', 'course': 2, 'phone': '+7-915-123-45-05'},
    {'username': 'kuznetsova_maria', 'email': 'kuznetsova.maria@student.ru', 'full_name': 'Кузнецова Мария Игоревна',
     'group': 'ИС-02', 'course': 2, 'phone': '+7-915-123-45-06'},
    {'username': 'petrov_alexey', 'email': 'petrov.alexey@student.ru', 'full_name': 'Петров Алексей Николаевич',
     'group': 'ИС-03', 'course': 3, 'phone': '+7-915-123-45-07'},
    {'username': 'mikhailova_olga', 'email': 'mikhailova.olga@student.ru', 'full_name': 'Михайлова Ольга Павловна',
     'group': 'ИС-03', 'course': 3, 'phone': '+7-915-123-45-08'},
    {'username': 'fedotov_andrey', 'email': 'fedotov.andrey@student.ru', 'full_name': 'Федотов Андрей Романович',
     'group': 'ИС-03', 'course': 3, 'phone': '+7-915-123-45-09'},
    {'username': 'grigorieva_tatyana', 'email': 'grigorieva.tatyana@student.ru',
     'full_name': 'Григорьева Татьяна Викторовна', 'group': 'ПИ-01', 'course': 4, 'phone': '+7-915-123-45-10'},
    {'username': 'nikolaev_sergey', 'email': 'nikolaev.sergey@student.ru', 'full_name': 'Николаев Сергей Александрович',
     'group': 'ПИ-01', 'course': 4, 'phone': '+7-915-123-45-11'},
    {'username': 'pavlova_yulia', 'email': 'pavlova.yulia@student.ru', 'full_name': 'Павлова Юлия Дмитриевна',
     'group': 'ПИ-01', 'course': 4, 'phone': '+7-915-123-45-12'},
    {'username': 'semenov_vladimir', 'email': 'semenov.vladimir@student.ru',
     'full_name': 'Семёнов Владимир Константинович', 'group': 'ПИ-02', 'course': 2, 'phone': '+7-915-123-45-13'},
    {'username': 'egorova_elena', 'email': 'egorova.elena@student.ru', 'full_name': 'Егорова Елена Михайловна',
     'group': 'ПИ-02', 'course': 2, 'phone': '+7-915-123-45-14'},
    {'username': 'tarasov_pavel', 'email': 'tarasov.pavel@student.ru', 'full_name': 'Тарасов Павел Андреевич',
     'group': 'БИ-01', 'course': 3, 'phone': '+7-915-123-45-15'},
    {'username': 'orlova_natalia', 'email': 'orlova.natalia@student.ru', 'full_name': 'Орлова Наталья Ильинична',
     'group': 'БИ-01', 'course': 3, 'phone': '+7-915-123-45-16'},
    {'username': 'kiselev_daniil', 'email': 'kiselev.daniil@student.ru', 'full_name': 'Киселёв Даниил Васильевич',
     'group': 'БИ-01', 'course': 3, 'phone': '+7-915-123-45-17'},
    {'username': 'vinogradova_anastasia', 'email': 'vinogradova.anastasia@student.ru',
     'full_name': 'Виноградова Анастасия Алексеевна', 'group': 'БИ-02', 'course': 1, 'phone': '+7-915-123-45-18'},
    {'username': 'gusev_artem', 'email': 'gusev.artem@student.ru', 'full_name': 'Гусев Артём Евгеньевич',
     'group': 'БИ-02', 'course': 1, 'phone': '+7-915-123-45-19'},
    {'username': 'efimova_darya', 'email': 'efimova.darya@student.ru', 'full_name': 'Ефимова Дарья Сергеевна',
     'group': 'БИ-02', 'course': 1, 'phone': '+7-915-123-45-20'},
]

with app.app_context():
    for s in students_data:
        # Проверяем, существует ли пользователь
        existing = User.query.filter_by(username=s['username']).first()
        if existing:
            print(f'Пользователь {s["username"]} уже существует, пропускаем.')
            continue

        # Создаём пользователя
        user = User(
            username=s['username'],
            email=s['email'],
            role='student'
        )
        user.set_password('student123')
        db.session.add(user)
        db.session.flush()  # Чтобы получить user.id

        # Создаём студента
        student = Student(
            user_id=user.id,
            full_name=s['full_name'],
            group_name=s['group'],
            course=s['course'],
            phone=s['phone'],
            student_card_number=f'ST{user.id:05d}'
        )
        db.session.add(student)
        print(f'Добавлен студент: {s["full_name"]} ({s["group"]}, {s["course"]} курс)')

    db.session.commit()
    print('\n✅ Готово! Добавлено 20 студентов.')
    print('\n📋 Логины и пароли для входа:')
    print('   Логин: любой из списка выше')
    print('   Пароль: student123')