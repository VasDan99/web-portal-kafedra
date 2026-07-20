from app import create_app, db
from app.models import Document
import sqlite3

app = create_app()

with app.app_context():
    # Подключаемся к базе данных
    conn = sqlite3.connect('instance/portal.db')
    cursor = conn.cursor()

    # Получаем список существующих колонок в таблице documents
    cursor.execute('PRAGMA table_info(documents)')
    existing_columns = [row[1] for row in cursor.fetchall()]

    print("Существующие колонки:", existing_columns)
    print("-" * 50)

    # Добавляем колонку status
    if 'status' not in existing_columns:
        cursor.execute('ALTER TABLE documents ADD COLUMN status TEXT DEFAULT "pending"')
        print('✅ Добавлена колонка status')
    else:
        print('⚠️ Колонка status уже существует')

    # Добавляем колонку review_comment
    if 'review_comment' not in existing_columns:
        cursor.execute('ALTER TABLE documents ADD COLUMN review_comment TEXT')
        print('✅ Добавлена колонка review_comment')
    else:
        print('⚠️ Колонка review_comment уже существует')

    # Добавляем колонку reviewed_at
    if 'reviewed_at' not in existing_columns:
        cursor.execute('ALTER TABLE documents ADD COLUMN reviewed_at TIMESTAMP')
        print('✅ Добавлена колонка reviewed_at')
    else:
        print('⚠️ Колонка reviewed_at уже существует')

    # Добавляем колонку reviewed_by
    if 'reviewed_by' not in existing_columns:
        cursor.execute('ALTER TABLE documents ADD COLUMN reviewed_by INTEGER REFERENCES users(id)')
        print('✅ Добавлена колонка reviewed_by')
    else:
        print('⚠️ Колонка reviewed_by уже существует')

    # Сохраняем изменения
    conn.commit()
    conn.close()

    print("\n" + "=" * 50)
    print("✅ База данных успешно обновлена!")
    print("=" * 50)

    # Проверяем результат
    conn = sqlite3.connect('instance/portal.db')
    cursor = conn.cursor()
    cursor.execute('PRAGMA table_info(documents)')
    columns = [row[1] for row in cursor.fetchall()]
    print("\n📋 Итоговый список колонок в таблице documents:")
    for col in columns:
        print(f"   - {col}")
    conn.close()