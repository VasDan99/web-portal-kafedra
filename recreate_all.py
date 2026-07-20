from app import create_app, db
from app.models import User, Student, Document, WorkMessage, Feedback, Grade, Schedule

app = create_app()

with app.app_context():
    print("=" * 60)
    print("ПЕРЕСОЗДАНИЕ БАЗЫ ДАННЫХ")
    print("=" * 60)
    
    # 1. Удаляем все сообщения (WorkMessage)
    print("\n1. Удаляем сообщения...")
    db.session.query(WorkMessage).delete()
    db.session.commit()
    
    # 2. Удаляем все работы
    print("2. Удаляем работы...")
    db.session.query(Document).delete()
    db.session.commit()
    
    # 3. Удаляем все оценки
    print("3. Удаляем оценки...")
    db.session.query(Grade).delete()
    db.session.commit()
    
    # 4. Удаляем все отзывы
    print("4. Удаляем отзывы...")
    db.session.query(Feedback).delete()
    db.session.commit()
    
    # 5. Удаляем расписание
    print("5. Удаляем расписание...")
    db.session.query(Schedule).delete()
    db.session.commit()
    
    # 6. Удаляем всех студентов
    print("6. Удаляем студентов...")
    db.session.query(Student).delete()
    db.session.commit()
    
    # 7. Удаляем всех пользователей с ролью student
    print("7. Удаляем пользователей-студентов...")
    users_to_delete = User.query.filter_by(role='student').all()
    for user in users_to_delete:
        db.session.delete(user)
    db.session.commit()
    
    print("✅ База очищена!")
    
    # 8. Создаём студентов
    print("\n8. Создаём студентов...")
    print("-" * 60)
    
    students_data = [
        ('belov_ivan', 'belov123', 'Белов Иван Андреевич', 'ИС-01', 1),
        ('volkova_anna', 'volkova123', 'Волкова Анна Сергеевна', 'ИС-01', 1),
        ('morozov_dmitry', 'morozov123', 'Морозов Дмитрий Алексеевич', 'ИС-01', 1),
        ('sokolova_ekaterina', 'sokolova123', 'Соколова Екатерина Владимировна', 'ИС-02', 2),
        ('kovalev_maxim', 'kovalev123', 'Ковалёв Максим Денисович', 'ИС-02', 2),
        ('kuznetsova_maria', 'kuznetsova123', 'Кузнецова Мария Игоревна', 'ИС-02', 2),
        ('petrov_alexey', 'petrov123', 'Петров Алексей Николаевич', 'ИС-03', 3),
        ('mikhailova_olga', 'mikhailova123', 'Михайлова Ольга Павловна', 'ИС-03', 3),
        ('fedotov_andrey', 'fedotov123', 'Федотов Андрей Романович', 'ИС-03', 3),
        ('grigorieva_tatyana', 'grigorieva123', 'Григорьева Татьяна Викторовна', 'ПИ-01', 4),
        ('nikolaev_sergey', 'nikolaev123', 'Николаев Сергей Александрович', 'ПИ-01', 4),
        ('pavlova_yulia', 'pavlova123', 'Павлова Юлия Дмитриевна', 'ПИ-01', 4),
        ('semenov_vladimir', 'semenov123', 'Семёнов Владимир Константинович', 'ПИ-02', 2),
        ('egorova_elena', 'egorova123', 'Егорова Елена Михайловна', 'ПИ-02', 2),
        ('tarasov_pavel', 'tarasov123', 'Тарасов Павел Андреевич', 'БИ-01', 3),
        ('orlova_natalia', 'orlova123', 'Орлова Наталья Ильинична', 'БИ-01', 3),
        ('kiselev_daniil', 'kiselev123', 'Киселёв Даниил Васильевич', 'БИ-01', 3),
        ('vinogradova_anastasia', 'vinogradova123', 'Виноградова Анастасия Алексеевна', 'БИ-02', 1),
        ('gusev_artem', 'gusev123', 'Гусев Артём Евгеньевич', 'БИ-02', 1),
        ('efimova_darya', 'efimova123', 'Ефимова Дарья Сергеевна', 'БИ-02', 1),
    ]
    
    for username, password, full_name, group_name, course in students_data:
        user = User(
            username=username,
            email=f'{username}@student.vitte.ru',
            role='student'
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()
        
        student = Student(
            user_id=user.id,
            full_name=full_name,
            group_name=group_name,
            course=course
        )
        db.session.add(student)
        print(f"✅ {full_name} → {username} (пароль: {password})")
    
    db.session.commit()
    
    print("-" * 60)
    print(f"✅ Создано {len(students_data)} студентов!")
    print("=" * 60)