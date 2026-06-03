import sqlite3
import os

db_path = os.path.join('instance', 'portal.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Пересоздаём таблицу work_messages с правильным nullable для work_id
cursor.execute('DROP TABLE IF EXISTS work_messages')
cursor.execute('''
CREATE TABLE work_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    work_id INTEGER,
    from_user_id INTEGER NOT NULL,
    to_user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    file_path VARCHAR(300),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT 0,
    reply TEXT,
    replied_at TIMESTAMP,
    FOREIGN KEY (work_id) REFERENCES documents (id),
    FOREIGN KEY (from_user_id) REFERENCES users (id),
    FOREIGN KEY (to_user_id) REFERENCES users (id)
)
''')
conn.commit()
print('Таблица work_messages пересоздана с nullable work_id')
conn.close()