import os
from app import create_app

os.makedirs('instance', exist_ok=True)

app = create_app()

# Выводим все маршруты для отладки
print("=== Зарегистрированные маршруты ===")
for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint}: {rule.methods} {rule}")

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)