from app import create_app, db
from app.models import User, Student, Document, WorkMessage, Feedback, Grade, Schedule

app = create_app()

with app.app_context():
    print("=" * 60)
    print("УДАЛЕНИЕ ВСЕХ СТУДЕНТОВ И РАБОТ")
    print("=" * 60)
    
    # 1. Удаляем все сообщения
    print("\n1. Удаляем сообщения...")
    db.session.query(WorkMessage).delete()
    db.session.commit()
    
    # 2. Удаляем все работы
    print("2. Удаляем работы...")
    db.session.query(Document).delete()
    db.session.commit()
    
    # 3. Удаляем все оценки
    print("3. Удаляем оценки...")
    db.session.query(Grade).delete()
    db.session.commit()
    
    # 4. Удаляем все отзывы
    print("4. Удаляем отзывы...")
    db.session.query(Feedback).delete()
    db.session.commit()
    
    # 5. Удаляем расписание
    print("5. Удаляем расписание...")
    db.session.query(Schedule).delete()
    db.session.commit()
    
    # 6. Удаляем всех студентов
    print("6. Удаляем студентов...")
    db.session.query(Student).delete()
    db.session.commit()
    
    # 7. Удаляем всех пользователей с ролью student
    print("7. Удаляем пользователей-студентов...")
    users = User.query.filter_by(role='student').all()
    for user in users:
        db.session.delete(user)
    db.session.commit()
    
    print("\n✅ Все студенты и работы удалены!")
    print("=" * 60)