from app import create_app, db
from app.models import User, Teacher, Discipline

app = create_app()

with app.app_context():
    print("=" * 60)
    print("Добавление преподавателя: Романова Ирина Петровна")
    print("=" * 60)
    
    # 1. Создаём пользователя
    user = User.query.filter_by(username="romanova").first()
    if not user:
        user = User(
            username="romanova",
            email="romanova@vitte.ru",
            role="teacher"
        )
        user.set_password("romanova123")
        db.session.add(user)
        db.session.flush()
        print("✅ Создан пользователь: romanova (пароль: romanova123)")
    else:
        print("⚠️ Пользователь romanova уже существует")
    
    # 2. Создаём преподавателя
    teacher = Teacher.query.filter_by(user_id=user.id).first()
    if not teacher:
        teacher = Teacher(
            user_id=user.id,
            full_name="Романова Ирина Петровна",
            department="Информационных технологий",
            position="Профессор",
            degree="Кандидат технических наук"
        )
        db.session.add(teacher)
        db.session.flush()
        print("✅ Создан преподаватель: Романова Ирина Петровна")
    else:
        print("⚠️ Преподаватель Романова И.П. уже существует")
    
    # 3. Добавляем дисциплины
    disciplines_to_add = ["Реляционные базы данных", "Интеллектуальный анализ данных"]
    
    for disc_name in disciplines_to_add:
        disc = Discipline.query.filter_by(name=disc_name).first()
        if not disc:
            disc = Discipline(
                name=disc_name,
                code=disc_name[:15].upper().replace(" ", "_"),
                teacher_id=teacher.id
            )
            db.session.add(disc)
            print(f"✅ Добавлена дисциплина: {disc_name}")
        else:
            disc.teacher_id = teacher.id
            print(f"✅ Обновлена дисциплина: {disc_name} (назначен преподаватель)")
    
    # Сохраняем
    db.session.commit()
    
    print("\n" + "=" * 60)
    print("ГОТОВО!")
    print("=" * 60)
    print("\n📋 Преподаватель Романова Ирина Петровна теперь ведёт:")
    for disc in disciplines_to_add:
        print(f"   • {disc}")