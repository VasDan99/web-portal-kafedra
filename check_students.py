import sqlite3

conn = sqlite3.connect('instance/portal.db')
cursor = conn.cursor()

# Проверяем соответствие пользователей и студентов
cursor.execute('''
    SELECT u.id, u.username, s.id as student_id, s.full_name
    FROM users u
    LEFT JOIN students s ON s.user_id = u.id
    WHERE u.role = 'student'
    ORDER BY u.id
''')
rows = cursor.fetchall()

print('Соответствие пользователей и студентов:')
for row in rows:
    print(f'  User ID: {row[0]}, Логин: {row[1]}, Student ID: {row[2]}, ФИО: {row[3]}')

# Проверяем работы
print('\n=== Работы и их владельцы ===')
cursor.execute('''
    SELECT d.id, d.title, u.username, s.full_name
    FROM documents d
    JOIN users u ON d.uploaded_by = u.id
    LEFT JOIN students s ON s.user_id = u.id
''')
rows = cursor.fetchall()
for row in rows:
    print(f'  Работа: {row[1]}, Владелец: {row[3]} (логин: {row[2]})')

conn.close()