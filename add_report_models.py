from app import create_app, db
import sqlite3

app = create_app()

with app.app_context():
    conn = sqlite3.connect('instance/portal.db')
    cursor = conn.cursor()
    
    # Создаём таблицы для отчётности
    tables = [
        ('reports', '''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teacher_id INTEGER NOT NULL,
                discipline_id INTEGER NOT NULL,
                group_name VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(20) DEFAULT 'draft',
                average_score FLOAT,
                success_rate FLOAT,
                debt_count INTEGER DEFAULT 0,
                FOREIGN KEY (teacher_id) REFERENCES users (id),
                FOREIGN KEY (discipline_id) REFERENCES disciplines (id)
            )
        '''),
        ('report_status_logs', '''
            CREATE TABLE IF NOT EXISTS report_status_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_id INTEGER NOT NULL,
                old_status VARCHAR(20),
                new_status VARCHAR(20) NOT NULL,
                user_id INTEGER NOT NULL,
                changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (report_id) REFERENCES reports (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        '''),
        ('report_comments', '''
            CREATE TABLE IF NOT EXISTS report_comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (report_id) REFERENCES reports (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        '''),
        ('teacher_disciplines', '''
            CREATE TABLE IF NOT EXISTS teacher_disciplines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teacher_id INTEGER NOT NULL,
                discipline_id INTEGER NOT NULL,
                FOREIGN KEY (teacher_id) REFERENCES users (id),
                FOREIGN KEY (discipline_id) REFERENCES disciplines (id),
                UNIQUE (teacher_id, discipline_id)
            )
        ''')
    ]
    
    for name, sql in tables:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (name,))
        if not cursor.fetchone():
            cursor.execute(sql)
            print(f'✅ Создана таблица {name}')
        else:
            print(f'⚠️ Таблица {name} уже существует')
    
    conn.commit()
    conn.close()
    print('✅ База данных обновлена!')