from app import create_app, db
from app.models import User, Teacher, Discipline

# Данные преподавателей
teachers_data = [
    {
        "full_name": "Атаева Ольга Муратовна",
        "username": "ataeva",
        "password": "ataeva123",
        "department": "Информационных технологий",
        "position": "Преподаватель",
        "disciplines": ["Искусственный интеллект"]
    },
    {
        "full_name": "Блощук Андрей Алексеевич",
        "username": "bloschuk",
        "password": "bloschuk123",
        "department": "Информационных технологий",
        "position": "Преподаватель",
        "disciplines": ["Компьютерные сети", "Управление IT проектами"]
    },
    {
        "full_name": "Имани Ханум Курбанкадыевна",
        "username": "imani",
        "password": "imani123",
        "department": "Информационных технологий",
        "position": "Преподаватель",
        "disciplines": ["Офисные приложения"]
    },
    {
        "full_name": "Киселев Федор Владимирович",
        "username": "kiselev",
        "password": "kiselev123",
        "department": "Информационных технологий",
        "position": "Преподаватель",
        "disciplines": ["Программирование", "Web-технологии", "Алгоритмизация"]
    },
    {
        "full_name": "Королькова Ирина Анатольевна",
        "username": "korolkova",
        "password": "korolkova123",
        "department": "Информационных технологий",
        "position": "Преподаватель",
        "disciplines": ["Базы данных", "Реляционные базы данных"]
    },
    {
        "full_name": "Преображенский Максим Владимирович",
        "username": "preobrazhensky",
        "password": "preobrazhensky123",
        "department": "Информационных технологий",
        "position": "Преподаватель",
        "disciplines": ["Высокоуровневые методы программирования"]
    },
    {
        "full_name": "Пузицкий Михаил Леонидович",
        "username": "puzitsky",
        "password": "puzitsky123",
        "department": "Информационных технологий",
        "position": "Преподаватель",
        "disciplines": []  # без дисциплин
    },
    {
        "full_name": "Стряпунина Нэля Ильинична",
        "username": "stryapunina",
        "password": "stryapunina123",
        "department": "Информационных технологий",
        "position": "Преподаватель",
        "disciplines": ["1С: Предприятие"]
    },
    {
        "full_name": "Сурина Елена Евгеньевна",
        "username": "surina",
        "password": "surina123",
        "department": "Информационных технологий",
        "position": "Преподаватель",
        "disciplines": ["Теория систем", "Эконометрика"]
    }
]

app = create_app()

with app.app_context():
    print("=" * 50)
    print("Добавление преподавателей и дисциплин")
    print("=" * 50)
    
    for teacher_data in teachers_data:
        # Проверяем, существует ли пользователь
        user = User.query.filter_by(username=teacher_data["username"]).first()
        
        if not user:
            # Создаём пользователя
            user = User(
                username=teacher_data["username"],
                email=f"{teacher_data['username']}@vitte.ru",
                role="teacher"
            )
            user.set_password(teacher_data["password"])
            db.session.add(user)
            db.session.flush()  # Получаем ID пользователя
            print(f"✅ Создан пользователь: {teacher_data['username']}")
        else:
            print(f"⚠️ Пользователь {teacher_data['username']} уже существует")
        
        # Проверяем, существует ли преподаватель
        teacher = Teacher.query.filter_by(user_id=user.id).first()
        
        if not teacher:
            # Создаём преподавателя
            teacher = Teacher(
                user_id=user.id,
                full_name=teacher_data["full_name"],
                department=teacher_data["department"],
                position=teacher_data["position"]
            )
            db.session.add(teacher)
            db.session.flush()
            print(f"✅ Добавлен преподаватель: {teacher_data['full_name']}")
        else:
            print(f"⚠️ Преподаватель {teacher_data['full_name']} уже существует")
        
        # Добавляем дисциплины
        for disc_name in teacher_data["disciplines"]:
            discipline = Discipline.query.filter_by(name=disc_name).first()
            
            if not discipline:
                discipline = Discipline(
                    name=disc_name,
                    code=disc_name[:10].upper().replace(" ", "_"),
                    teacher_id=teacher.id
                )
                db.session.add(discipline)
                print(f"  📚 Добавлена дисциплина: {disc_name}")
            else:
                # Обновляем teacher_id если дисциплина без преподавателя
                if discipline.teacher_id is None:
                    discipline.teacher_id = teacher.id
                    print(f"  📚 Обновлена дисциплина: {disc_name} (назначен преподаватель)")
                else:
                    print(f"  ⚠️ Дисциплина {disc_name} уже существует")
        
        print("-" * 30)
    
    # Сохраняем все изменения
    db.session.commit()
    
    print("\n" + "=" * 50)
    print("ГОТОВО!")
    print("=" * 50)
    
    # Выводим статистику
    print(f"\n📊 Статистика:")
    print(f"   Пользователей (учителя): {User.query.filter_by(role='teacher').count()}")
    print(f"   Преподавателей: {Teacher.query.count()}")
    print(f"   Дисциплин: {Discipline.query.count()}")
    
    # Показываем всех преподавателей
    print("\n📋 Список преподавателей:")
    teachers = Teacher.query.all()
    for t in teachers:
        disciplines = Discipline.query.filter_by(teacher_id=t.id).all()
        disc_names = [d.name for d in disciplines]
        print(f"   • {t.full_name} — {', '.join(disc_names) if disc_names else 'нет дисциплин'}")