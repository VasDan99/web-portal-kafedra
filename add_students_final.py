from app import create_app, db
from app.models import User, Student

app = create_app()

with app.app_context():
    print("=" * 60)
    print("ДОБАВЛЕНИЕ СТУДЕНТОВ В БАЗУ ДАННЫХ")
    print("=" * 60)
    
    # Список студентов: логин, пароль, ФИО, группа, курс
    students_data = [
        ('sidorov_petr', 'sidorov123', 'Сидоров Пётр Алексеевич', 'ИС-01', 1),
        ('kuzmin_ivan', 'kuzmin123', 'Кузьмин Иван Сергеевич', 'ИС-01', 1),
        ('makarova_elena', 'makarova123', 'Макарова Елена Владимировна', 'ИС-01', 1),
        ('popov_andrey', 'popov123', 'Попов Андрей Николаевич', 'ИС-02', 2),
        ('smirnova_olga', 'smirnova123', 'Смирнова Ольга Петровна', 'ИС-02', 2),
        ('novikov_dmitry', 'novikov123', 'Новиков Дмитрий Александрович', 'ИС-02', 2),
        ('fedorova_natalia', 'fedorova123', 'Фёдорова Наталья Игоревна', 'ИС-03', 3),
        ('morozov_sergey', 'morozov123', 'Морозов Сергей Владимирович', 'ИС-03', 3),
        ('vasilieva_anna', 'vasilieva123', 'Васильева Анна Михайловна', 'ИС-03', 3),
        ('koltsov_alexey', 'koltsov123', 'Кольцов Алексей Сергеевич', 'ПИ-01', 4),
        ('tereshkina_maria', 'tereshkina123', 'Терешкина Мария Дмитриевна', 'ПИ-01', 4),
        ('zaitsev_pavel', 'zaitsev123', 'Зайцев Павел Андреевич', 'ПИ-01', 4),
        ('orlov_vladimir', 'orlov123', 'Орлов Владимир Игоревич', 'ПИ-02', 2),
        ('kravtsova_elena', 'kravtsova123', 'Кравцова Елена Сергеевна', 'ПИ-02', 2),
        ('lobanov_anton', 'lobanov123', 'Лобанов Антон Евгеньевич', 'БИ-01', 3),
    ]
    
    created_count = 0
    skipped_count = 0
    
    for username, password, full_name, group_name, course in students_data:
        # Проверяем, существует ли пользователь
        user = User.query.filter_by(username=username).first()
        
        if not user:
            # Создаём пользователя
            user = User(
                username=username,
                email=f'{username}@student.vitte.ru',
                role='student'
            )
            user.set_password(password)
            db.session.add(user)
            db.session.flush()
            
            # Создаём студента
            student = Student(
                user_id=user.id,
                full_name=full_name,
                group_name=group_name,
                course=course
            )
            db.session.add(student)
            print(f'✅ {full_name} → {username} (пароль: {password})')
            created_count += 1
        else:
            print(f'⚠️ {full_name} (логин: {username}) уже существует')
            skipped_count += 1
    
    db.session.commit()
    
    print("-" * 60)
    print(f'✅ СОЗДАНО: {created_count} студентов')
    print(f'⚠️ ПРОПУЩЕНО: {skipped_count} студентов (уже существовали)')
    print("=" * 60)
    
    # Показываем итоговый список
    print("\n📋 Итоговый список студентов:")
    students = Student.query.all()
    for s in students:
        user = User.query.get(s.user_id)
        print(f'  {s.full_name} → {user.username} (группа: {s.group_name}, курс: {s.course})')