from app import create_app, db
import sqlite3

app = create_app()

with app.app_context():
    conn = sqlite3.connect('instance/portal.db')
    cursor = conn.cursor()
    
    # Добавляем поле is_active в таблицу users
    cursor.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'is_active' not in columns:
        cursor.execute('ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 0')
        print('✅ Добавлено поле is_active в users')
    else:
        print('⚠️ Поле is_active уже существует')
    
    # Создаём таблицу registration_requests
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='registration_requests'")
    if not cursor.fetchone():
        cursor.execute('''
            CREATE TABLE registration_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                full_name VARCHAR(150) NOT NULL,
                group_name VARCHAR(50) NOT NULL,
                course INTEGER NOT NULL,
                phone VARCHAR(20),
                status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reviewed_at TIMESTAMP,
                reviewed_by INTEGER,
                review_comment TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (reviewed_by) REFERENCES users (id)
            )
        ''')
        print('✅ Создана таблица registration_requests')
    else:
        print('⚠️ Таблица registration_requests уже существует')
    
    conn.commit()
    conn.close()
    print('✅ База данных обновлена!')