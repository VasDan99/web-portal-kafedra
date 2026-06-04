import sqlite3
import os

db_path = '/tmp/portal.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS site_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_title VARCHAR(200),
    site_description VARCHAR(500),
    email VARCHAR(120),
    phone VARCHAR(50),
    address VARCHAR(300),
    work_hours VARCHAR(200),
    vk_url VARCHAR(200),
    telegram_url VARCHAR(200),
    primary_color VARCHAR(20),
    secondary_color VARCHAR(20),
    accent_color VARCHAR(20),
    logo_path VARCHAR(200),
    about_text TEXT,
    updated_at TIMESTAMP
)
''')
conn.commit()
print('Таблица site_settings создана!')

# Добавляем начальную запись
cursor.execute('SELECT COUNT(*) FROM site_settings')
count = cursor.fetchone()[0]
if count == 0:
    cursor.execute('''
    INSERT INTO site_settings (
        site_title, site_description, email, phone, address, work_hours,
        vk_url, telegram_url, primary_color, secondary_color, accent_color,
        logo_path, about_text, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'Кафедра информационных систем',
        'Московский университет имени Витте',
        'is@vitte.ru',
        '+7 (495) 123-45-67',
        'г. Москва, ул. Косыгина, д. 15',
        'Пн-Пт: 9:00 - 18:00',
        'https://vk.com/vitte',
        'https://t.me/vitte',
        '#003366',
        '#005599',
        '#28a745',
        '/static/images/logo.png',
        '',
        None
    ))
    conn.commit()
    print('Начальные настройки добавлены!')

conn.close()
print('Готово!')