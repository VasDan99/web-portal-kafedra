from app import create_app, db
from app.models import User, Teacher, Discipline

app = create_app()

with app.app_context():
    print("=" * 70)
    print("СОЗДАНИЕ ВСЕХ ПРЕПОДАВАТЕЛЕЙ И ДИСЦИПЛИН")
    print("=" * 70)
    
    # Данные преподавателей
    teachers_data = [
        {
            'username': 'surina',
            'password': 'surina123',
            'full_name': 'Сурина Елена Евгеньевна',
            'department': 'Информационных технологий',
            'position': 'Заведующий кафедрой МиЕНД, доцент кафедры ИС',
            'degree': 'Кандидат экономических наук',
            'disciplines': ['Теория систем и системный анализ', 'Методы оптимизации', 'Эконометрика', 'Статистические методы веб-аналитики']
        },
        {
            'username': 'korolkova',
            'password': 'korolkova123',
            'full_name': 'Королькова Ирина Анатольевна',
            'department': 'Информационных технологий',
            'position': 'Руководитель образовательной программы, старший преподаватель',
            'degree': None,
            'disciplines': ['Проектирование пользовательских интерфейсов']
        },
        {
            'username': 'ataeva',
            'password': 'ataeva123',
            'full_name': 'Атаева Ольга Муратовна',
            'department': 'Информационных технологий',
            'position': 'Старший научный сотрудник, доцент',
            'degree': 'Кандидат технических наук',
            'disciplines': ['Прикладные задачи анализа данных']
        },
        {
            'username': 'puzitsky',
            'password': 'puzitsky123',
            'full_name': 'Пузицкий Михаил Леонидович',
            'department': 'Информационных технологий',
            'position': 'Преподаватель',
            'degree': None,
            'disciplines': []
        },
        {
            'username': 'romanova',
            'password': 'romanova123',
            'full_name': 'Романова Ирина Петровна',
            'department': 'Информационных технологий',
            'position': 'Доцент кафедры',
            'degree': 'Кандидат технических наук',
            'disciplines': ['Реляционные базы данных', 'Интеллектуальный анализ данных']
        },
        {
            'username': 'bloschuk',
            'password': 'bloschuk123',
            'full_name': 'Блощук Андрей Алексеевич',
            'department': 'Информационных технологий',
            'position': 'Доцент кафедры',
            'degree': 'Кандидат технических наук',
            'disciplines': ['Управление ИТ проектами', 'Проектная деятельность в ИТ']
        },
        {
            'username': 'imani',
            'password': 'imani123',
            'full_name': 'Имани Ханум Курбанкадыевна',
            'department': 'Информационных технологий',
            'position': 'Старший преподаватель',
            'degree': None,
            'disciplines': ['Офисные приложения и совместная работа с документами', 'Информационно-аналитические системы']
        },
        {
            'username': 'kiselev',
            'password': 'kiselev123',
            'full_name': 'Киселев Федор Владимирович',
            'department': 'Информационных технологий',
            'position': 'Старший преподаватель кафедры',
            'degree': None,
            'disciplines': ['Алгоритмизация и программирование', 'Веб-разработка']
        },
        {
            'username': 'preobrazhensky',
            'password': 'preobrazhensky123',
            'full_name': 'Преображенский Максим Владимирович',
            'department': 'Информационных технологий',
            'position': 'Старший преподаватель',
            'degree': None,
            'disciplines': ['Высокоуровневые методы программирования']
        },
        {
            'username': 'stryapunina',
            'password': 'stryapunina123',
            'full_name': 'Стряпунина Нэля Ильинична',
            'department': 'Информационных технологий',
            'position': 'Старший преподаватель кафедры',
            'degree': None,
            'disciplines': ['Конфигурирование на платформе 1С: Предприятие', 'Информационные системы управления бизнесом и взаимоотношениями с клиентами']
        },
    ]
    
    created_count = 0
    updated_count = 0
    
    for teacher_data in teachers_data:
        username = teacher_data['username']
        
        user = User.query.filter_by(username=username).first()
        
        if not user:
            user = User(
                username=username,
                email=f'{username}@vitte.ru',
                role='teacher'
            )
            user.set_password(teacher_data['password'])
            db.session.add(user)
            db.session.flush()
            print(f'✅ Создан пользователь: {username} (пароль: {teacher_data["password"]})')
            created_count += 1
        else:
            print(f'⚠️ Пользователь {username} уже существует')
            updated_count += 1
        
        teacher = Teacher.query.filter_by(user_id=user.id).first()
        
        if not teacher:
            teacher = Teacher(
                user_id=user.id,
                full_name=teacher_data['full_name'],
                department=teacher_data['department'],
                position=teacher_data['position'],
                degree=teacher_data['degree']
            )
            db.session.add(teacher)
            db.session.flush()
            print(f'✅ Создан преподаватель: {teacher_data["full_name"]}')
        else:
            teacher.full_name = teacher_data['full_name']
            teacher.department = teacher_data['department']
            teacher.position = teacher_data['position']
            teacher.degree = teacher_data['degree']
            print(f'✅ Обновлён преподаватель: {teacher_data["full_name"]}')
        
        for disc_name in teacher_data['disciplines']:
            disc = Discipline.query.filter_by(name=disc_name).first()
            if not disc:
                # Используем ID для создания уникального кода
                import hashlib
                unique_code = hashlib.md5(disc_name.encode()).hexdigest()[:10].upper()
                disc = Discipline(
                    name=disc_name,
                    code=unique_code,
                    teacher_id=teacher.id
                )
                db.session.add(disc)
                print(f'  📚 Добавлена дисциплина: {disc_name}')
            else:
                if disc.teacher_id != teacher.id:
                    disc.teacher_id = teacher.id
                    print(f'  📚 Обновлена дисциплина: {disc_name} (назначен преподаватель)')
                else:
                    print(f'  ⚠️ Дисциплина {disc_name} уже есть у этого преподавателя')
        
        print("-" * 50)
    
    db.session.commit()
    
    print("=" * 70)
    print(f'✅ СОЗДАНО: {created_count} преподавателей')
    print(f'⚠️ ОБНОВЛЕНО: {updated_count} преподавателей')
    print("=" * 70)
    
    print("\n📋 Итоговый список преподавателей:")
    teachers = Teacher.query.all()
    for t in teachers:
        user = User.query.get(t.user_id)
        disciplines = Discipline.query.filter_by(teacher_id=t.id).all()
        disc_names = [d.name for d in disciplines]
        print(f'  {t.full_name} → {user.username} ({", ".join(disc_names) if disc_names else "нет дисциплин"})')