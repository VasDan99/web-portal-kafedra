import sqlite3
import os

db_path = os.path.join('instance', 'portal.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Проверяем, есть ли колонка bio в таблице teachers
cursor.execute("PRAGMA table_info(teachers)")
columns = [col[1] for col in cursor.fetchall()]

if 'bio' not in columns:
    cursor.execute('ALTER TABLE teachers ADD COLUMN bio TEXT')
    conn.commit()
    print('Поле bio добавлено в таблицу teachers')
else:
    print('Поле bio уже существует в таблице teachers')

# Проверяем результат
cursor.execute("PRAGMA table_info(teachers)")
print("\nКолонки в таблице teachers:")
for col in cursor.fetchall():
    print(f'  {col[1]} - {col[2]}')

conn.close()
print('\nГотово!')