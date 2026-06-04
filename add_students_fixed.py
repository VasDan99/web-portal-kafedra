from app import create_app, db
from app.models import User, Student

# Данные студентов
students_data = [
    ("belov_ivan", "Белов Иван Андреевич", "ИС-01", 1),
    ("volkova_anna", "Волкова Анна Сергеевна", "ИС-01", 1),
    ("morozov_dmitry", "Морозов Дмитрий Алексеевич", "ИС-01", 1),
    ("sokolova_ekaterina", "Соколова Екатерина Владимировна", "ИС-02", 2),
    ("kovalev_maxim", "Ковалёв Максим Денисович", "ИС-02", 2),
    ("kuznetsova_maria", "Кузнецова Мария Игоревна", "ИС-02", 2),
    ("petrov_alexey", "Петров Алексей Николаевич", "ИС-03", 3),
    ("mikhailova_olga", "Михайлова Ольга Павловна", "ИС-03", 3),
    ("fedotov_andrey", "Федотов Андрей Романович", "ИС-03", 3),
    ("grigorieva_tatyana", "Григорьева Татьяна Викторовна", "ПИ-01", 4),
    ("nikolaev_sergey", "Николаев Сергей Александрович", "ПИ-01", 4),
    ("pavlova_yulia", "Павлова Юлия Дмитриевна", "ПИ-01", 4),
    ("semenov_vladimir", "Семёнов Владимир Константинович", "ПИ-02", 2),
    ("egorova_elena", "Егорова Елена Михайловна", "ПИ-02", 2),
    ("tarasov_pavel", "Тарасов Павел Андреевич", "БИ-01", 3),
    ("orlova_natalia", "Орлова Наталья Ильинична", "БИ-01", 3),
    ("kiselev_daniil", "Киселёв Даниил Васильевич", "БИ-01", 3),
    ("vinogradova_anastasia", "Виноградова Анастасия Алексеевна", "БИ-02", 1),
    ("gusev_artem", "Гусев Артём Евгеньевич", "БИ-02", 1),
    ("efimova_darya", "Ефимова Дарья Сергеевна", "БИ-02", 1),
]

app = create_app()

with app.app_context():
    print("Создание студентов...")
    print("=" * 50)
    
    for username, full_name, group_name, course in students_data:
        # Проверяем, существует ли пользователь
        user = User.query.filter_by(username=username).first()
        
        if not user:
            # Пароль = фамилия + 123 (берём первую часть логина)
            password = username.split("_")[0] + "123"
            
            # Создаём пользователя
            user = User(
                username=username,
                email=f"{username}@student.vitte.ru",
                role="student"
            )
            user.set_password(password)
            db.session.add(user)
            db.session.flush()
            print(f"[OK] Создан пользователь: {username} (пароль: {password})")
            
            # Создаём студента
            student = Student(
                user_id=user.id,
                full_name=full_name,
                group_name=group_name,
                course=course
            )
            db.session.add(student)
            print(f"     Студент: {full_name} | {group_name} | {course} курс")
        else:
            print(f"[!] Пользователь {username} уже существует")
        
        print("-" * 40)
    
    # Сохраняем изменения
    db.session.commit()
    
    print("\n" + "=" * 50)
    print("ИТОГО:")
    students_count = User.query.filter_by(role="student").count()
    print(f"  Всего студентов в базе: {students_count}")
    print("=" * 50)
    
    print("\n" + "=" * 50)
    print("СПИСОК ДЛЯ ВХОДА:")
    print("=" * 50)
    for username, full_name, group_name, course in students_data:
        password = username.split("_")[0] + "123"
        print(f"  {username} | {password} | {full_name}")
    print("=" * 50)