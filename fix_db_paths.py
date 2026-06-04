import os
import re

files_to_fix = [
    'add_bio_column.py',
    'add_image_column.py',
    'add_max_column.py',
    'add_reply_column.py',
    'add_site_settings.py',
    'create_workmessage_table.py',
    'fix_database.py',
    'fix_roles.py',
    'fix_teachers_table.py',
    'fix_workmessage_table.py',
    'update_workmessage.py'
]

for filename in files_to_fix:
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Заменяем пути к БД
        content = content.replace("os.path.join('instance', 'portal.db')", "'/tmp/portal.db'")
        content = content.replace("'instance/portal.db'", "'/tmp/portal.db'")

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Исправлен: {filename}')
    else:
        print(f'Не найден: {filename}')

print('Готово!')