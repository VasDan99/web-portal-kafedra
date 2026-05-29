from flask import render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from app.main import bp
from app.forms import FeedbackForm, StudentProfileForm
from app.models import Feedback, Student, Teacher, Discipline, Grade, Schedule
from app import db
import os
from datetime import datetime


# ==================== Публичные страницы ====================

@bp.route('/')
def index():
    breadcrumb_title = None
    return render_template('index.html', breadcrumb_title=breadcrumb_title)

@bp.route('/about')
def about():
    breadcrumb_title = 'О факультете ИТ'
    return render_template('about.html', breadcrumb_title=breadcrumb_title)

@bp.route('/history')
def history():
    breadcrumb_title = 'История факультета'
    return render_template('history.html', breadcrumb_title=breadcrumb_title)

@bp.route('/mission')
def mission():
    breadcrumb_title = 'Миссия и цели'
    return render_template('mission.html', breadcrumb_title=breadcrumb_title)

@bp.route('/team')
def team():
    breadcrumb_title = 'Команда факультета'
    return render_template('team.html', breadcrumb_title=breadcrumb_title)

@bp.route('/departments')
def departments():
    breadcrumb_title = 'Кафедры факультета'
    return render_template('departments.html', breadcrumb_title=breadcrumb_title)

@bp.route('/teachers')
def teachers():
    breadcrumb_title = 'Преподаватели'
    return render_template('teachers.html', breadcrumb_title=breadcrumb_title)

@bp.route('/disciplines')
def disciplines():
    breadcrumb_title = 'Дисциплины'
    return render_template('disciplines.html', breadcrumb_title=breadcrumb_title)

@bp.route('/discipline/<int:disc_id>')
def discipline_detail(disc_id):
    disciplines_data = {
        1: {'name': 'Программирование', 'description': 'Изучение языков программирования, алгоритмов и структур данных.'},
        2: {'name': 'Базы данных', 'description': 'Проектирование, разработка и администрирование баз данных.'},
        3: {'name': 'Web-технологии', 'description': 'Разработка веб-приложений на современных фреймворках.'},
        4: {'name': 'Искусственный интеллект', 'description': 'Нейронные сети, машинное обучение и анализ данных.'}
    }
    disc = disciplines_data.get(disc_id, {'name': 'Дисциплина', 'description': 'Описание'})
    breadcrumb_title = disc['name']
    return render_template('discipline_detail.html', breadcrumb_title=breadcrumb_title, discipline=disc)

@bp.route('/schedule')
def schedule():
    breadcrumb_title = 'Расписание занятий'
    return render_template('schedule.html', breadcrumb_title=breadcrumb_title)

@bp.route('/science-works')
def science_works():
    breadcrumb_title = 'Научные работы'
    return render_template('science_works.html', breadcrumb_title=breadcrumb_title)

@bp.route('/contacts')
def contacts():
    breadcrumb_title = 'Контакты'
    return render_template('contacts.html', breadcrumb_title=breadcrumb_title)

@bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    breadcrumb_title = 'Обратная связь'
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback_entry = Feedback(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(feedback_entry)
        db.session.commit()
        flash('Ваше сообщение отправлено! Спасибо за обратную связь.', 'success')
        return redirect(url_for('main.feedback'))
    return render_template('feedback.html', breadcrumb_title=breadcrumb_title, form=form)

@bp.route('/admin')
def admin():
    breadcrumb_title = 'Админ-панель'
    messages = Feedback.query.order_by(Feedback.created_at.desc()).all()
    return render_template('admin/index.html', breadcrumb_title=breadcrumb_title, messages=messages)


# ==================== Личный кабинет студента ====================

@bp.route('/cabinet/student/profile')
@login_required
def student_profile():
    if current_user.role != 'student':
        abort(403)
    student = Student.query.filter_by(user_id=current_user.id).first()
    if not student:
        student = Student(user_id=current_user.id, full_name=current_user.username, group_name='ИС-01', course=1)
        db.session.add(student)
        db.session.commit()
    return render_template('cabinet/student_profile.html', breadcrumb_title='Мой профиль', student=student)

@bp.route('/cabinet/student/profile/edit', methods=['GET', 'POST'])
@login_required
def student_profile_edit():
    if current_user.role != 'student':
        abort(403)
    student = Student.query.filter_by(user_id=current_user.id).first()
    form = StudentProfileForm()

    if form.validate_on_submit():
        student.full_name = form.full_name.data
        student.group_name = form.group_name.data
        student.course = int(form.course.data)
        student.phone = form.phone.data
        student.telegram = form.telegram.data
        student.bio = form.bio.data

        if form.avatar.data:
            avatar_file = form.avatar.data
            filename = f'user_{current_user.id}.jpg'
            os.makedirs('app/static/uploads/avatars', exist_ok=True)
            filepath = os.path.join('app/static/uploads/avatars', filename)
            avatar_file.save(filepath)
            student.avatar = f'/static/uploads/avatars/{filename}'

        db.session.commit()
        flash('Профиль обновлён!', 'success')
        return redirect(url_for('main.student_profile'))

    form.full_name.data = student.full_name
    form.group_name.data = student.group_name
    form.course.data = str(student.course)
    form.phone.data = student.phone
    form.telegram.data = student.telegram
    form.bio.data = student.bio

    return render_template('cabinet/student_profile_edit.html', breadcrumb_title='Редактирование профиля', form=form, student=student)

@bp.route('/cabinet/student/grades')
@login_required
def student_grades():
    if current_user.role != 'student':
        abort(403)
    student = Student.query.filter_by(user_id=current_user.id).first()
    grades = Grade.query.filter_by(student_id=student.id).all() if student else []
    return render_template('cabinet/student_grades.html', breadcrumb_title='Мои оценки', grades=grades, student=student)

@bp.route('/cabinet/student/schedule')
@login_required
def student_schedule():
    if current_user.role != 'student':
        abort(403)
    student = Student.query.filter_by(user_id=current_user.id).first()
    schedule = Schedule.query.filter_by(group_name=student.group_name).all() if student else []
    return render_template('cabinet/student_schedule.html', breadcrumb_title='Моё расписание', schedule=schedule, student=student)

@bp.route('/cabinet/student/works')
@login_required
def student_works():
    if current_user.role != 'student':
        abort(403)
    student = Student.query.filter_by(user_id=current_user.id).first()
    return render_template('cabinet/student_works.html', breadcrumb_title='Мои работы', student=student)

@bp.route('/cabinet/student/works/upload', methods=['POST'])
@login_required
def student_works_upload():
    if current_user.role != 'student':
        abort(403)

    file = request.files.get('file')
    title = request.form.get('title')

    if file and title:
        os.makedirs('app/static/uploads/works', exist_ok=True)
        filename = f'work_{current_user.id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        filepath = os.path.join('app/static/uploads/works', filename)
        file.save(filepath)

        from app.models import Document
        work = Document(
            title=title,
            filename=filename,
            file_path=f'/static/uploads/works/{filename}',
            uploaded_by=current_user.id,
            is_public=False
        )
        db.session.add(work)
        db.session.commit()
        flash('Работа загружена!', 'success')

    return redirect(url_for('main.student_works'))

@bp.route('/cabinet/student/achievements')
@login_required
def student_achievements():
    if current_user.role != 'student':
        abort(403)
    student = Student.query.filter_by(user_id=current_user.id).first()
    return render_template('cabinet/student_achievements.html', breadcrumb_title='Мои достижения', student=student)

@bp.route('/cabinet/student/teachers')
@login_required
def student_teachers():
    if current_user.role != 'student':
        abort(403)
    student = Student.query.filter_by(user_id=current_user.id).first()
    teachers = Teacher.query.all()
    return render_template('cabinet/student_teachers.html', breadcrumb_title='Мои преподаватели', teachers=teachers, student=student)

@bp.route('/cabinet/student/ask_teacher/<int:teacher_id>', methods=['GET', 'POST'])
@login_required
def ask_teacher(teacher_id):
    if current_user.role != 'student':
        abort(403)

    teacher = Teacher.query.get_or_404(teacher_id)
    student = Student.query.filter_by(user_id=current_user.id).first()

    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            feedback = Feedback(
                name=student.full_name,
                email=current_user.email,
                subject=f'Вопрос преподавателю {teacher.full_name}',
                message=message,
                status='for_teacher'
            )
            db.session.add(feedback)
            db.session.commit()
            flash('Вопрос отправлен преподавателю!', 'success')
            return redirect(url_for('main.student_teachers'))

    return render_template('cabinet/ask_teacher.html', breadcrumb_title='Задать вопрос', teacher=teacher, student=student)

@bp.route('/cabinet/student/documents')
@login_required
def student_documents():
    if current_user.role != 'student':
        abort(403)
    student = Student.query.filter_by(user_id=current_user.id).first()
    return render_template('cabinet/student_documents.html', breadcrumb_title='Мои документы', student=student)

@bp.route('/cabinet/student/settings')
@login_required
def student_settings():
    if current_user.role != 'student':
        abort(403)
    student = Student.query.filter_by(user_id=current_user.id).first()
    return render_template('cabinet/student_settings.html', breadcrumb_title='Настройки', student=student)


# ==================== Личный кабинет преподавателя ====================

@bp.route('/cabinet/teacher/profile')
@login_required
def teacher_profile():
    if current_user.role != 'teacher':
        abort(403)
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher:
        teacher = Teacher(user_id=current_user.id, full_name=current_user.username, department='ИТ', position='Преподаватель')
        db.session.add(teacher)
        db.session.commit()
    return render_template('cabinet/teacher/profile.html', breadcrumb_title='Мой профиль', teacher=teacher)

@bp.route('/cabinet/teacher/disciplines')
@login_required
def teacher_disciplines():
    if current_user.role != 'teacher':
        abort(403)
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    disciplines = Discipline.query.filter_by(teacher_id=teacher.id).all() if teacher else []
    return render_template('cabinet/teacher/disciplines.html', breadcrumb_title='Мои дисциплины', disciplines=disciplines, teacher=teacher)

@bp.route('/cabinet/teacher/students')
@login_required
def teacher_students():
    if current_user.role != 'teacher':
        abort(403)
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    students = Student.query.all()
    return render_template('cabinet/teacher/students.html', breadcrumb_title='Студенты', students=students, teacher=teacher)

@bp.route('/cabinet/teacher/reports')
@login_required
def teacher_reports():
    if current_user.role != 'teacher':
        abort(403)
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    return render_template('cabinet/teacher/reports.html', breadcrumb_title='Отчёты', teacher=teacher)

@bp.route('/cabinet/teacher/settings')
@login_required
def teacher_settings():
    if current_user.role != 'teacher':
        abort(403)
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    return render_template('cabinet/teacher/settings.html', breadcrumb_title='Настройки', teacher=teacher)