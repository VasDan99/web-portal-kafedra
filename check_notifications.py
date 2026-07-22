import sqlite3

conn = sqlite3.connect('instance/portal.db')
cursor = conn.cursor()

# Проверяем, существует ли таблица notifications
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='notifications'")
result = cursor.fetchone()

if result:
    print('✅ Таблица notifications существует')
else:
    print('❌ Таблицы notifications нет')
    print('Создаём таблицу...')
    
    cursor.execute('''
        CREATE TABLE notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title VARCHAR(200) NOT NULL,
            message TEXT NOT NULL,
            is_read BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            link VARCHAR(200),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    print('✅ Таблица notifications создана!')

conn.close()