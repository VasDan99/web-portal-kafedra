from app import create_app, db
from app.models import Document
import sqlite3

app = create_app()

with app.app_context():
    # Добавляем колонку file_type, если её нет
    try:
        db.session.execute('ALTER TABLE documents ADD COLUMN file_type VARCHAR(20) DEFAULT "pdf"')
        db.session.commit()
        print('Поле file_type добавлено')
    except:
        print('Поле file_type уже существует')

    print('База данных обновлена')