import sqlite3
import os

db_path = os.path.join('instance', 'portal.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Удаляем старую таблицу teachers и создаём заново с nullable user_id
cursor.execute("DROP TABLE IF EXISTS teachers")
cursor.execute('''
CREATE TABLE teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    full_name VARCHAR(150) NOT NULL,
    department VARCHAR(100) NOT NULL,
    position VARCHAR(100),
    degree VARCHAR(100),
    phone VARCHAR(20),
    avatar VARCHAR(200),
    bio TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')
conn.commit()
print('Таблица teachers пересоздана с nullable user_id')

conn.close()
print('Готово!')