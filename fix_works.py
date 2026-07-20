import sqlite3

conn = sqlite3.connect('instance/portal.db')
cursor = conn.cursor()

# Находим ID Белова
cursor.execute('SELECT id FROM users WHERE username = "belov_ivan"')
belov_row = cursor.fetchone()

if belov_row:
    belov_id = belov_row[0]
    print(f'ID Белова: {belov_id}')
    
    # Обновляем все работы
    cursor.execute('UPDATE documents SET uploaded_by = ?', (belov_id,))
    conn.commit()
    print('Все работы перенесены к Белову!')
else:
    print('Белов не найден!')

# Проверяем результат
cursor.execute('''
    SELECT d.id, d.title, u.username, s.full_name
    FROM documents d
    JOIN users u ON d.uploaded_by = u.id
    LEFT JOIN students s ON s.user_id = u.id
''')
rows = cursor.fetchall()
print('\nРаботы после обновления:')
for row in rows:
    print(f'  {row[1]} → {row[3]} (логин: {row[2]})')

conn.close()