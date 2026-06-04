import sqlite3
import os

db_path = '/tmp/portal.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute('ALTER TABLE site_settings ADD COLUMN max_url VARCHAR(200)')
    conn.commit()
    print('Поле max_url добавлено в таблицу site_settings')
except sqlite3.OperationalError as e:
    if 'duplicate column name' in str(e):
        print('Поле max_url уже существует')
    else:
        print(f'Ошибка: {e}')

conn.close()
print('Готово!')