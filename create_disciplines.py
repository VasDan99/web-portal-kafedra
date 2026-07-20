from app import create_app, db
from app.models import Discipline, Teacher

app = create_app()

with app.app_context():
    print("=" * 60)
    print("СОЗДАНИЕ ДИСЦИПЛИН")
    print("=" * 60)
    
    # Список дисциплин
    disciplines = [
        'Программирование',
        'Web-технологии',
        'Базы данных',
        'Реляционные базы данных',
        'Искусственный интеллект',
        'Интеллектуальный анализ данных',
        'Компьютерные сети',
        'Управление IT проектами',
        'Офисные приложения',
        'Алгоритмизация',
        'Высокоуровневые методы программирования',
        'Теория систем',
        'Эконометрика',
        '1С: Предприятие',
    ]
    
    # Находим первого преподавателя (админа или любого)
    teacher = Teacher.query.first()
    if not teacher:
        print('❌ Преподаватели не найдены!')
        print('Сначала добавьте преподавателей.')
        exit()
    
    print(f'✅ Найден преподаватель: {teacher.full_name} (ID: {teacher.id})')
    
    for disc_name in disciplines:
        disc = Discipline.query.filter_by(name=disc_name).first()
        if not disc:
            disc = Discipline(
                name=disc_name,
                code=disc_name[:10].upper().replace(' ', '_'),
                teacher_id=teacher.id
            )
            db.session.add(disc)
            print(f'✅ Добавлена дисциплина: {disc_name}')
        else:
            print(f'⚠️ Дисциплина {disc_name} уже существует')
    
    db.session.commit()
    
    print("-" * 60)
    print(f'✅ Создано {len(disciplines)} дисциплин!')
    print("=" * 60)