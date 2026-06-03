import sqlite3
import os

db_path = os.path.join('instance', 'portal.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute('ALTER TABLE news ADD COLUMN image_url VARCHAR(300)')
    conn.commit()
    print('Поле image_url добавлено в таблицу news')
except sqlite3.OperationalError as e:
    if 'duplicate column name' in str(e):
        print('Поле image_url уже существует')
    else:
        print(f'Ошибка: {e}')

conn.close()
print('Готово!')