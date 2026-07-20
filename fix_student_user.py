import sqlite3

conn = sqlite3.connect('instance/portal.db')
cursor = conn.cursor()

# 1. Проверяем студентов
print("=== Текущие студенты ===")
cursor.execute('''
    SELECT id, user_id, full_name 
    FROM students 
    WHERE full_name LIKE "%Павлова%" OR full_name LIKE "%Белов%"
''')
rows = cursor.fetchall()
for row in rows:
    print(f'  ID: {row[0]}, user_id: {row[1]}, ФИО: {row[2]}')

# 2. Находим правильный user_id для Белова
cursor.execute('SELECT id FROM users WHERE username = "belov_ivan"')
belov_row = cursor.fetchone()

if belov_row:
    belov_user_id = belov_row[0]
    print(f'\n✅ Правильный user_id для belov_ivan: {belov_user_id}')
    
    # 3. Обновляем user_id в таблице students
    cursor.execute('''
        UPDATE students 
        SET user_id = ? 
        WHERE full_name = "Белов Иван Андреевич"
    ''', (belov_user_id,))
    conn.commit()
    print(f'✅ Обновлён user_id для Белова на {belov_user_id}')
else:
    print('❌ Пользователь belov_ivan не найден!')
    exit()

# 4. Проверяем результат
print("\n=== После обновления ===")
cursor.execute('''
    SELECT id, user_id, full_name 
    FROM students 
    WHERE full_name LIKE "%Белов%"
''')
row = cursor.fetchone()
if row:
    print(f'  ✅ ID: {row[0]}, user_id: {row[1]}, ФИО: {row[2]}')

# 5. Проверяем работы
print("\n=== Работы и их владельцы ===")
cursor.execute('''
    SELECT d.id, d.title, u.username, s.full_name
    FROM documents d
    JOIN users u ON d.uploaded_by = u.id
    LEFT JOIN students s ON s.user_id = u.id
''')
rows = cursor.fetchall()
for row in rows:
    print(f'  Работа: {row[1]} → {row[3]} (логин: {row[2]})')

conn.close()
print("\n✅ Готово!")