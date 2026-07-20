import sqlite3

conn = sqlite3.connect('instance/portal.db')
cursor = conn.cursor()

# Список студентов с их логинами
students = [
    ('belov_ivan', 'Белов Иван Андреевич'),
    ('volkova_anna', 'Волкова Анна Сергеевна'),
    ('morozov_dmitry', 'Морозов Дмитрий Алексеевич'),
    ('sokolova_ekaterina', 'Соколова Екатерина Владимировна'),
    ('kovalev_maxim', 'Ковалёв Максим Денисович'),
    ('kuznetsova_maria', 'Кузнецова Мария Игоревна'),
    ('petrov_alexey', 'Петров Алексей Николаевич'),
    ('mikhailova_olga', 'Михайлова Ольга Павловна'),
    ('fedotov_andrey', 'Федотов Андрей Романович'),
    ('grigorieva_tatyana', 'Григорьева Татьяна Викторовна'),
    ('nikolaev_sergey', 'Николаев Сергей Александрович'),
    ('pavlova_yulia', 'Павлова Юлия Дмитриевна'),
    ('semenov_vladimir', 'Семёнов Владимир Константинович'),
    ('egorova_elena', 'Егорова Елена Михайловна'),
    ('tarasov_pavel', 'Тарасов Павел Андреевич'),
    ('orlova_natalia', 'Орлова Наталья Ильинична'),
    ('kiselev_daniil', 'Киселёв Даниил Васильевич'),
    ('vinogradova_anastasia', 'Виноградова Анастасия Алексеевна'),
    ('gusev_artem', 'Гусев Артём Евгеньевич'),
    ('efimova_darya', 'Ефимова Дарья Сергеевна'),
]

# Получаем ID всех студентов
student_ids = {}
for username, full_name in students:
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    if row:
        student_ids[username] = row[0]
        print(f'✅ {full_name} → ID: {row[0]}')
    else:
        print(f'❌ {username} не найден!')

print('\n' + '='*50)

# Получаем все работы
cursor.execute('SELECT id, title, uploaded_by FROM documents')
works = cursor.fetchall()

print(f'Найдено работ: {len(works)}')
print('\nТекущие владельцы:')
for work in works:
    cursor.execute('SELECT username FROM users WHERE id = ?', (work[2],))
    user = cursor.fetchone()
    print(f'  Работа "{work[1]}" → пользователь: {user[0] if user else "неизвестно"}')

print('\n' + '='*50)
print('Выберите, как переназначить работы:')
print('1 — Всем работам назначить Белова (для теста)')
print('2 — Назначить каждую работу случайному студенту')
print('3 — Ввести номера работ и студентов вручную')

choice = input('Ваш выбор (1/2/3): ')

if choice == '1':
    # Назначаем все работы Белову
    belov_id = student_ids.get('belov_ivan')
    if belov_id:
        cursor.execute('UPDATE documents SET uploaded_by = ?', (belov_id,))
        print(f'✅ Все работы назначены Белову (ID: {belov_id})')
    else:
        print('❌ Белов не найден!')

elif choice == '2':
    # Назначаем работы по очереди
    import random
    student_list = list(student_ids.values())
    for work in works:
        random_student = random.choice(student_list)
        cursor.execute('UPDATE documents SET uploaded_by = ? WHERE id = ?', (random_student, work[0]))
        print(f'  Работа ID {work[0]} → студент ID {random_student}')
    print('✅ Все работы переназначены случайным образом')

elif choice == '3':
    print('Введите пары: ID_работы ID_студента (например: 1 4)')
    print('Для завершения введите пустую строку')
    while True:
        line = input('> ')
        if not line:
            break
        try:
            work_id, student_id = map(int, line.split())
            if student_id in student_ids.values():
                cursor.execute('UPDATE documents SET uploaded_by = ? WHERE id = ?', (student_id, work_id))
                print(f'✅ Работа ID {work_id} → студент ID {student_id}')
            else:
                print(f'❌ Студент ID {student_id} не найден')
        except:
            print('❌ Неверный формат! Используйте: ID_работы ID_студента')

conn.commit()
print('\n' + '='*50)
print('✅ Готово!')

# Проверяем результат
cursor.execute('''
    SELECT d.id, d.title, u.username, s.full_name
    FROM documents d
    JOIN users u ON d.uploaded_by = u.id
    LEFT JOIN students s ON s.user_id = u.id
''')
rows = cursor.fetchall()
print('\n📋 Итоговый список:')
for row in rows:
    print(f'  {row[1]} → {row[3]} (логин: {row[2]})')

conn.close()