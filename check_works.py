import sqlite3

conn = sqlite3.connect('instance/portal.db')
cursor = conn.cursor()

# Проверяем, кто владелец работ
cursor.execute('''
    SELECT d.id, d.title, d.uploaded_by, u.username, s.full_name
    FROM documents d
    JOIN users u ON d.uploaded_by = u.id
    LEFT JOIN students s ON s.user_id = u.id
''')
rows = cursor.fetchall()
print('Работы в базе:')
for row in rows:
    print(f'  ID: {row[0]}, Название: {row[1]}, Владелец: {row[4]} (логин: {row[3]})')
conn.close()