from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime


# Таблица 1: Пользователи
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


# Таблица 2: Студенты
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    full_name = db.Column(db.String(150), nullable=False)
    group_name = db.Column(db.String(50), nullable=False)
    course = db.Column(db.Integer, nullable=False)
    student_card_number = db.Column(db.String(20), unique=True)
    phone = db.Column(db.String(20))
    avatar = db.Column(db.String(200), default='/static/images/default-avatar.png')
    bio = db.Column(db.Text)
    telegram = db.Column(db.String(100))

    user = db.relationship('User', backref='student_profile', uselist=False)

    def get_average_grade(self):
        """Рассчитывает средний балл студента по всем оценкам"""
        grades = Grade.query.filter_by(student_id=self.id).all()
        if not grades:
            return None
        total = sum(g.grade_value for g in grades)
        return round(total / len(grades), 2)

    def get_grades_by_discipline(self, discipline_id):
        """Возвращает все оценки студента по конкретной дисциплине"""
        return Grade.query.filter_by(student_id=self.id, discipline_id=discipline_id).all()

    def get_discipline_average(self, discipline_id):
        """Средний балл по конкретной дисциплине"""
        grades = self.get_grades_by_discipline(discipline_id)
        if not grades:
            return None
        total = sum(g.grade_value for g in grades)
        return round(total / len(grades), 2)

    def get_attendance_stats(self):
        """Статистика по дисциплинам: сдано/не сдано"""
        # Получаем все дисциплины
        all_disciplines = Discipline.query.all()
        stats = {}

        for disc in all_disciplines:
            grades = Grade.query.filter_by(student_id=self.id, discipline_id=disc.id).all()
            if grades:
                # Если есть хотя бы одна оценка — считаем, что дисциплина сдана
                stats[disc.name] = {
                    'status': 'Сдана',
                    'grades': [g.grade_value for g in grades],
                    'average': round(sum(g.grade_value for g in grades) / len(grades), 2),
                    'discipline_id': disc.id
                }
            else:
                stats[disc.name] = {
                    'status': 'Не сдана',
                    'grades': [],
                    'average': None,
                    'discipline_id': disc.id
                }
        return stats

    def get_debts(self):
        """Возвращает список дисциплин, по которым есть задолженности"""
        stats = self.get_attendance_stats()
        debts = []
        for disc_name, data in stats.items():
            if data['status'] == 'Не сдана':
                debts.append({
                    'name': disc_name,
                    'discipline_id': data['discipline_id']
                })
        return debts

    def get_total_credits(self):
        """Общее количество дисциплин"""
        return Discipline.query.count()

    def get_completed_credits(self):
        """Количество сданных дисциплин"""
        stats = self.get_attendance_stats()
        completed = sum(1 for data in stats.values() if data['status'] == 'Сдана')
        return completed

    def get_progress_percentage(self):
        """Процент успеваемости (сдано / всего дисциплин * 100)"""
        total = self.get_total_credits()
        if total == 0:
            return 0
        completed = self.get_completed_credits()
        return round((completed / total) * 100, 1)


# Таблица 3: Преподаватели
class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    full_name = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100))
    degree = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    avatar = db.Column(db.String(200), default='/static/images/default-avatar.png')
    bio = db.Column(db.Text)

    user = db.relationship('User', backref='teacher_profile', uselist=False)


# Таблица 4: Дисциплины
class Discipline(db.Model):
    __tablename__ = 'disciplines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(20), unique=True)
    description = db.Column(db.Text)
    hours = db.Column(db.Integer)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))

    teacher = db.relationship('Teacher', backref='disciplines')


# Таблица 5: Новости
class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    author = db.relationship('User', backref='news')


# Таблица 6: Мероприятия
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Таблица 7: Документы
class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(300), nullable=False)
    file_type = db.Column(db.String(20), default='pdf')
    file_size = db.Column(db.Integer)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'))
    is_public = db.Column(db.Boolean, default=False)

    # ===== НОВЫЕ ПОЛЯ ДЛЯ ПРОВЕРКИ РАБОТ =====
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    review_comment = db.Column(db.Text)  # Комментарий преподавателя
    reviewed_at = db.Column(db.DateTime)  # Дата проверки
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # Кто проверил

    # Связи
    reviewer = db.relationship('User', foreign_keys=[reviewed_by], backref='reviewed_documents')


# Таблица 8: Обратная связь
class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='new')
    reply = db.Column(db.Text)
    replied_at = db.Column(db.DateTime)


# Таблица 9: Оценки
class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'), nullable=False)
    grade_value = db.Column(db.Integer, nullable=False)
    grade_type = db.Column(db.String(50))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))

    student = db.relationship('Student', backref='grades')
    discipline = db.relationship('Discipline', backref='grades')


# Таблица 10: Расписание
class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True)
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'), nullable=False)
    group_name = db.Column(db.String(50), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)
    lesson_time = db.Column(db.String(20), nullable=False)
    classroom = db.Column(db.String(50))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))

    discipline = db.relationship('Discipline', backref='schedule')
    teacher = db.relationship('Teacher', backref='schedule')


# Таблица 11: Сообщения по работам
class WorkMessage(db.Model):
    __tablename__ = 'work_messages'
    id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    reply = db.Column(db.Text)
    replied_at = db.Column(db.DateTime)

    work = db.relationship('Document', backref='messages')
    from_user = db.relationship('User', foreign_keys=[from_user_id], backref='sent_messages')
    to_user = db.relationship('User', foreign_keys=[to_user_id], backref='received_messages')


# Таблица 12: Настройки сайта
class SiteSettings(db.Model):
    __tablename__ = 'site_settings'
    id = db.Column(db.Integer, primary_key=True)

    site_title = db.Column(db.String(200), default='Кафедра информационных систем')
    site_description = db.Column(db.String(500), default='Московский университет имени Витте')
    email = db.Column(db.String(120), default='is@vitte.ru')
    phone = db.Column(db.String(50), default='+7 (495) 123-45-67')
    address = db.Column(db.String(300), default='г. Москва, ул. Косыгина, д. 15')
    work_hours = db.Column(db.String(200), default='Пн-Пт: 9:00 - 18:00')
    vk_url = db.Column(db.String(200), default='https://vk.com/vitte')
    telegram_url = db.Column(db.String(200), default='https://t.me/vitte')
    max_url = db.Column(db.String(200), default='')
    primary_color = db.Column(db.String(20), default='#003366')
    secondary_color = db.Column(db.String(20), default='#005599')
    accent_color = db.Column(db.String(20), default='#28a745')
    logo_path = db.Column(db.String(200), default='/static/images/logo.png')
    about_text = db.Column(db.Text, default='')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)