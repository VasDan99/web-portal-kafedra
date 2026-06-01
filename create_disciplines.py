from app import create_app, db
from app.models import Discipline

app = create_app()

disciplines_data = [
    {'name': 'Программирование', 'code': 'PR01', 'hours': 144},
    {'name': 'Базы данных', 'code': 'DB01', 'hours': 108},
    {'name': 'Web-технологии', 'code': 'WEB01', 'hours': 108},
    {'name': 'Искусственный интеллект', 'code': 'AI01', 'hours': 72},
    {'name': 'Компьютерные сети', 'code': 'NET01', 'hours': 108},
    {'name': 'Офисные приложения', 'code': 'OFF01', 'hours': 72},
    {'name': '1С: Предприятие', 'code': 'ONE01', 'hours': 108},
    {'name': 'Управление IT проектами', 'code': 'PM01', 'hours': 72},
    {'name': 'Алгоритмизация', 'code': 'ALG01', 'hours': 108},
    {'name': 'Реляционные базы данных', 'code': 'RDB01', 'hours': 108},
]

with app.app_context():
    for d in disciplines_data:
        existing = Discipline.query.filter_by(name=d['name']).first()
        if not existing:
            discipline = Discipline(
                name=d['name'],
                code=d['code'],
                hours=d['hours']
            )
            db.session.add(discipline)
            print(f'Добавлена дисциплина: {d["name"]}')
        else:
            print(f'Уже существует: {d["name"]}')

    db.session.commit()
    print('\nГотово! Дисциплины созданы.')