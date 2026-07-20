import sqlite3

conn = sqlite3.connect('instance/portal.db')
cursor = conn.cursor()

# 1. Показываем всех студентов с их ID
print("=== Студенты ===")
cursor.execute('''
    SELECT u.id, u.username, s.full_name 
    FROM users u 
    JOIN students s ON s.user_id = u.id 
    WHERE u.role = 'student'
    ORDER BY u.id
''')
students = cursor.fetchall()
for student in students:
    print(f"  ID: {student[0]}, Логин: {student[1]}, ФИО: {student[2]}")

print("\n" + "="*50)

# 2. Показываем текущие работы
print("\n=== Текущие работы ===")
cursor.execute('''
    SELECT d.id, d.title, d.uploaded_by, u.username, s.full_name
    FROM documents d
    JOIN users u ON d.uploaded_by = u.id
    LEFT JOIN students s ON s.user_id = u.id
''')
works = cursor.fetchall()
for work in works:
    print(f"  ID: {work[0]}, Название: {work[1]}, Владелец: {work[4] or 'Неизвестно'} (логин: {work[3]})")

print("\n" + "="*50)

# 3. Создаём словарь соответствия: ID работы → ID студента
print("\nНазначаем работы студентам:")
updates = []

# Получаем ID каждого студента по логину
student_ids = {student[1]: student[0] for student in students}

# Здесь вы можете вручную указать, какая работа кому принадлежит
# Формат: (ID_работы, логин_студента)
assignments = [
    (1, 'belov_ivan'),      # Индивидуальное задание → Белов
    (2, 'belov_ivan'),      # Руководство → Белов
    (3, 'volkova_anna'),    # Руководство → Волкова
    # Добавьте сюда остальные работы, если они есть
]

for work_id, username in assignments:
    if username in student_ids:
        student_id = student_ids[username]
        cursor.execute('UPDATE documents SET uploaded_by = ? WHERE id = ?', (student_id, work_id))
        updates.append((work_id, username, student_id))
        print(f"  ✅ Работа ID {work_id} → {username} (ID: {student_id})")
    else:
        print(f"  ⚠️ Студент {username} не найден!")

conn.commit()

print("\n" + "="*50)

# 4. Проверяем результат
print("\n=== Работы после обновления ===")
cursor.execute('''
    SELECT d.id, d.title, u.username, s.full_name
    FROM documents d
    JOIN users u ON d.uploaded_by = u.id
    LEFT JOIN students s ON s.user_id = u.id
''')
works = cursor.fetchall()
for work in works:
    print(f"  ID: {work[0]}, Название: {work[1]}, Владелец: {work[3] or 'Неизвестно'} ({work[2]})")

conn.close()
print("\n✅ Готово!")