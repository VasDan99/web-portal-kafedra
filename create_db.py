from app import create_app, db
from app.models import User, Student, Teacher, Discipline, News, Event, Document, Feedback, Grade, Schedule, WorkMessage, SiteSettings

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Все таблицы созданы!")
    
    # Проверяем
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"📊 Создано таблиц: {len(tables)}")
    print(f"📋 Таблицы: {', '.join(tables)}")