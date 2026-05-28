from app import create_app, db
from app.models import User, Student, Teacher, Discipline, News, Event, Document, Feedback, Grade, Schedule

app = create_app()

with app.app_context():
    db.create_all()
    print("База данных обновлена!")
    print("Таблицы:", list(db.metadata.tables.keys()))