import sqlite3
import os

db_path = '/tmp/portal.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute('ALTER TABLE work_messages ADD COLUMN reply TEXT')
    print('Поле reply добавлено')
except sqlite3.OperationalError as e:
    print(f'Ошибка при добавлении reply: {e}')

try:
    cursor.execute('ALTER TABLE work_messages ADD COLUMN replied_at TIMESTAMP')
    print('Поле replied_at добавлено')
except sqlite3.OperationalError as e:
    print(f'Ошибка при добавлении replied_at: {e}')

conn.commit()
conn.close()
print('Готово!')