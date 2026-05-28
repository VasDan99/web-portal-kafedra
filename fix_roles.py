import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('instance/portal.db')
cursor = conn.cursor()

# Проверяем текущие роли
print("Текущие роли:")
cursor.execute("SELECT username, role FROM users")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

# Исправляем роли
cursor.execute("UPDATE users SET role = 'teacher' WHERE username = 'petrov_teacher'")
cursor.execute("UPDATE users SET role = 'admin' WHERE username = 'admin'")

# Сохраняем изменения
conn.commit()

# Проверяем исправленные роли
print("\nИсправленные роли:")
cursor.execute("SELECT username, role FROM users")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

# Закрываем соединение
conn.close()
print("\nГотово! Роли исправлены.")