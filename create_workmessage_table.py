import sqlite3
import os

db_path = '/tmp/portal.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Создаём таблицу work_messages
cursor.execute('''
CREATE TABLE IF NOT EXISTS work_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    work_id INTEGER NOT NULL,
    from_user_id INTEGER NOT NULL,
    to_user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    file_path VARCHAR(300),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT 0,
    FOREIGN KEY (work_id) REFERENCES documents (id),
    FOREIGN KEY (from_user_id) REFERENCES users (id),
    FOREIGN KEY (to_user_id) REFERENCES users (id)
)
''')
conn.commit()
print('Таблица work_messages создана!')

conn.close()