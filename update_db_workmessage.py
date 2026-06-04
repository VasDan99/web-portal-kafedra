from app import create_app, db
from app.models import WorkMessage

app = create_app()

with app.app_context():
    db.create_all()
    print('Таблица work_messages создана!')
