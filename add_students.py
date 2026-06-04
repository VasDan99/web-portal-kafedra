from app import create_app, db
from app.models import User, Student
from datetime import datetime

# Данные студентов
students_data = [
    {"full_name": "Белов Иван Андреевич", "group": "ИС-01", "course": 1, "username": "belov_ivan"},
    {"full_name": "Волкова Анна Сергеевна", "group": "ИС-01", "course": 1, "username": "volkova_anna"},
    {"full_name": "Морозов Дмитрий Алексеевич", "group": "ИС-01", "course": 1, "username": "morozov_dmitry"},
    {"full_name": "Соколова Екатерина Владимировна", "group": "ИС-02", "course": 2, "username": "sokolova_ekaterina"},
    {"full_name": "Ковалёв Максим Денисович", "group": "ИС-02", "course": 2, "username": "kovalev_maxim"},
    {"full_name": "Кузнецова Мария Игоревна", "group": "ИС-02", "course": 2, "username": "kuznetsova_maria"},
    {"full_name": "Петров Алексей Николаевич", "group": "ИС-03", "course": 3, "username": "petrov_alexey"},
    {"full_name": "Михайлова Ольга Павловна", "group": "ИС-03", "course": 3, "username": "mikhailova_olga"},
    {"full_name": "Федотов Андрей Романович", "group": "ИС-03", "course": 3, "username": "fedotov_andrey"},
    {"full_name": "Григорьева Татьяна Викторовна", "group": "ПИ-01", "course": 4, "username": "grigorieva_tatyana"},
    {"full_name": "Николаев Сергей Александрович", "group": "ПИ-01", "course": 4, "username": "nikolaev_sergey"},
    {"full_name": "Павлова Юлия Дмитриевна", "group": "ПИ-01", "course": 4, "username": "pavlova_yulia"},
    {"full_name": "Семёнов Владимир Константинович", "group": "ПИ-02", "course": 2, "username": "semenov_vladimir"},
    {"full_name": "Егорова Елена Михайловна", "group": "ПИ-02", "course": 2, "username": "egorova_elena"},
    {"full_name": "Тарасов Павел Андреевич", "group": "БИ-01", "course": 3, "username": "tarasov_pavel"},
    {"full_name": "Орлова Наталья Ильинична", "group": "БИ-01", "course": 3, "username": "orlova_natalia"},
    {"full_name": "Киселёв Даниил Васильевич", "group": "БИ-01", "course": 3, "username": "kiselev_daniil"},
    {"full_name": "Виноградова Анастасия Алексеевна", "group": "БИ-02", "course": 1, "username": "vinogradova_anastasia"},
    {"full_name": "Гусев Артём Евгеньевич", "group": "БИ-02", "course": 1, "username": "gusev_artem"},
    {"full_name": "Ефимова Дарья Сергеевна", "group": "БИ-02", "course": 1, "username": "efimova_darya"},
]

# Генерация пароля (по умолчанию: фамилия + 123)
def generate_password(full_name):
    # Берём фамилию (первое слово)
    last_name = full_name.split()[0].lower()
    return f"{last_name}123"

app = create_app()

with app.app_context():
    print("=" * 60)
    print("Добавление студентов")
    print("=" * 60)
    
    added_count = 0
    skipped_count = 0
    
    for student_data in students_data:
        username = student_data["username"]
        full_name = student_data["full_name"]
        password = generate_password(full_name)
        
        # Проверяем, существует ли пользователь
        user = User.query.filter_by(username=username).first()
        
        if not user:
            # Создаём пользователя
            user = User(
                username=username,
                email=f"{username}@student.vitte.ru",
                role="student"
            )
            user.set_password(password)
            db.session.add(user)
            db.session.flush()  # Получаем ID пользователя
            print(f"✅ Создан пользователь: {username} (пароль: {password})")
            
            # Создаём студента
            student = Student(
                user_id=user.id,
                full_name=full_name,
                group_name=student_data["group"],
                course=student_data["course"],
                student_card_number=f"СТ-{student_data['course']:02d}{username[-4:]}",
                phone="",
                avatar="/static/images/default-avatar.png"
            )
            db.session.add(student)
            print(f"   📚 Добавлен студент: {full_name} | Группа: {student_data['group']} | Курс: {student_data['course']}")
            added_count += 1
        else:
            print(f"⚠️ Пользователь {username} уже существует, пропускаем")
            skipped_count += 1
        
        print("-" * 40)
    
    # Сохраняем все изменения
    db.session.commit()
    
    print("\n" + "=" * 60)
    print("ГОТОВО!")
    print("=" * 60)
    
    # Выводим статистику
    print(f"\n📊 Статистика:")
    print(f"   Добавлено студентов: {added_count}")
    print(f"   Пропущено (уже есть): {skipped_count}")
    print(f"   Всего студентов в БД: {Student.query.count()}")
    print(f"   Всего пользователей (студенты): {User.query.filter_by(role='student').count()}")
    
    # Показываем всех студентов
    print("\n📋 Список студентов с паролями:")
    print("-" * 60)
    print(f"{'№':<3} {'ФИО':<35} {'Группа':<8} {'Логин':<20} {'Пароль':<15}")
    print("-" * 60)
    
    students = Student.query.all()
    for i, student in enumerate(students, 1):
        user = User.query.get(student.user_id)
        password = generate_password(student.full_name)
        print(f"{i:<3} {student.full_name:<35} {student.group_name:<8} {user.username:<20} {password:<15}")
    
    print("-" * 60)