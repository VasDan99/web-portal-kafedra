from app import create_app, db
from app.models import User, Student, Teacher, Discipline, News, Event, Document, Feedback, Grade, Schedule

app = create_app()

with app.app_context():
    db.create_all()
    print("База данных с 10 таблицами успешно создана!")
    print("Таблицы:", db.metadata.tables.keys())