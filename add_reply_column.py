import sqlite3
import os

db_path = '/tmp/portal.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute('ALTER TABLE feedback ADD COLUMN reply TEXT')
    print('Поле reply добавлено')
except sqlite3.OperationalError as e:
    if 'duplicate column name' in str(e):
        print('Поле reply уже существует')
    else:
        print(f'Ошибка: {e}')

try:
    cursor.execute('ALTER TABLE feedback ADD COLUMN replied_at TIMESTAMP')
    print('Поле replied_at добавлено')
except sqlite3.OperationalError as e:
    if 'duplicate column name' in str(e):
        print('Поле replied_at уже существует')
    else:
        print(f'Ошибка: {e}')

conn.commit()
conn.close()
print('Готово!')