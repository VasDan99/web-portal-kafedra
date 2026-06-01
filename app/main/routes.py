from flask import render_template, redirect, url_for, flash, abort, request, send_file
from flask_login import login_required, current_user
from app.main import bp
from app.forms import FeedbackForm, StudentProfileForm, WorkUploadForm, DocumentUploadForm, ChangePasswordForm
from app.models import Feedback, Student, Teacher, Discipline, Grade, Schedule, Document
from app import db
import os
from datetime import datetime
from io import BytesIO
from docx import Document as DocxDocument


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
    works = Document.query.filter_by(uploaded_by=current_user.id).all()
    form = WorkUploadForm()
    teachers = Teacher.query.all()
    form.teacher_id.choices = [(t.id, t.full_name) for t in teachers]
    return render_template('cabinet/student_works.html', breadcrumb_title='Мои работы', student=student, form=form, works=works)

@bp.route('/cabinet/student/works/upload', methods=['GET', 'POST'])
@login_required
def student_works_upload():
    if current_user.role != 'student':
        abort(403)
    student = Student.query.filter_by(user_id=current_user.id).first()
    form = WorkUploadForm()

    teachers = Teacher.query.all()
    form.teacher_id.choices = [(t.id, t.full_name) for t in teachers]

    if form.validate_on_submit():
        file = form.file.data
        filename = f'work_{current_user.id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        os.makedirs('app/static/uploads/works', exist_ok=True)
        filepath = os.path.join('app/static/uploads/works', filename)
        file.save(filepath)

        file_type = 'pdf'
        if filename.endswith('.docx'):
            file_type = 'docx'
        elif filename.endswith('.xlsx'):
            file_type = 'xlsx'

        work = Document(
            title=form.title.data,
            filename=filename,
            file_path=f'/static/uploads/works/{filename}',
            file_type=file_type,
            uploaded_by=current_user.id,
            discipline_id=form.teacher_id.data,
            is_public=False
        )
        db.session.add(work)
        db.session.commit()
        flash('Работа успешно загружена!', 'success')
        return redirect(url_for('main.student_works'))

    works = Document.query.filter_by(uploaded_by=current_user.id).all()
    return render_template('cabinet/student_works.html', breadcrumb_title='Мои работы', student=student, form=form, works=works)

@bp.route('/cabinet/student/work/delete/<int:work_id>')
@login_required
def student_work_delete(work_id):
    if current_user.role != 'student':
        abort(403)
    work = Document.query.get_or_404(work_id)
    if work.uploaded_by == current_user.id:
        filepath = os.path.join('app', work.file_path.lstrip('/'))
        if os.path.exists(filepath):
            os.remove(filepath)
        db.session.delete(work)
        db.session.commit()
        flash('Работа удалена!', 'success')
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
    documents = Document.query.filter_by(uploaded_by=current_user.id).all()
    form = DocumentUploadForm()
    return render_template('cabinet/student_documents.html', breadcrumb_title='Мои документы', student=student, form=form, documents=documents)

@bp.route('/cabinet/student/documents/upload', methods=['GET', 'POST'])
@login_required
def student_documents_upload():
    if current_user.role != 'student':
        abort(403)
    student = Student.query.filter_by(user_id=current_user.id).first()
    form = DocumentUploadForm()

    if form.validate_on_submit():
        file = form.file.data
        filename = f'doc_{current_user.id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}_{file.filename}'
        os.makedirs('app/static/uploads/documents', exist_ok=True)
        filepath = os.path.join('app/static/uploads/documents', filename)
        file.save(filepath)

        doc = Document(
            title=form.title.data,
            filename=filename,
            file_path=f'/static/uploads/documents/{filename}',
            uploaded_by=current_user.id,
            is_public=False
        )
        db.session.add(doc)
        db.session.commit()
        flash('Документ успешно загружен!', 'success')
        return redirect(url_for('main.student_documents'))

    documents = Document.query.filter_by(uploaded_by=current_user.id).all()
    return render_template('cabinet/student_documents.html', breadcrumb_title='Мои документы', student=student, form=form, documents=documents)

@bp.route('/cabinet/student/document/delete/<int:doc_id>')
@login_required
def student_document_delete(doc_id):
    if current_user.role != 'student':
        abort(403)
    doc = Document.query.get_or_404(doc_id)
    if doc.uploaded_by == current_user.id:
        filepath = os.path.join('app', doc.file_path.lstrip('/'))
        if os.path.exists(filepath):
            os.remove(filepath)
        db.session.delete(doc)
        db.session.commit()
        flash('Документ удалён!', 'success')
    return redirect(url_for('main.student_documents'))

@bp.route('/cabinet/student/generate/certificate')
@login_required
def generate_certificate():
    if current_user.role != 'student':
        abort(403)
    student = Student.query.filter_by(user_id=current_user.id).first()

    doc = DocxDocument()
    doc.add_heading('Справка об обучении', 0)
    doc.add_paragraph(f'Выдана студенту: {student.full_name}')
    doc.add_paragraph(f'Группа: {student.group_name}, {student.course} курс')
    doc.add_paragraph(f'Факультет информационных технологий')
    doc.add_paragraph(f'Московский университет имени Витте')
    doc.add_paragraph(f'Дата выдачи: {datetime.now().strftime("%d.%m.%Y")}')

    byte_io = BytesIO()
    doc.save(byte_io)
    byte_io.seek(0)

    return send_file(byte_io, as_attachment=True, download_name=f'spravka_{student.student_card_number}.docx')

@bp.route('/cabinet/student/settings', methods=['GET', 'POST'])
@login_required
def student_settings():
    if current_user.role != 'student':
        abort(403)
    student = Student.query.filter_by(user_id=current_user.id).first()
    password_form = ChangePasswordForm()
    profile_form = StudentProfileForm()

    if password_form.validate_on_submit() and password_form.submit.data:
        if current_user.check_password(password_form.current_password.data):
            if password_form.new_password.data == password_form.confirm_password.data:
                current_user.set_password(password_form.new_password.data)
                db.session.commit()
                flash('Пароль успешно изменён!', 'success')
            else:
                flash('Новые пароли не совпадают!', 'danger')
        else:
            flash('Неверный текущий пароль!', 'danger')
        return redirect(url_for('main.student_settings'))

    if profile_form.validate_on_submit() and profile_form.submit.data:
        student.full_name = profile_form.full_name.data
        student.group_name = profile_form.group_name.data
        student.course = int(profile_form.course.data)
        student.phone = profile_form.phone.data
        student.telegram = profile_form.telegram.data
        student.bio = profile_form.bio.data

        if profile_form.avatar.data:
            avatar_file = profile_form.avatar.data
            filename = f'avatar_{current_user.id}.jpg'
            os.makedirs('app/static/uploads/avatars', exist_ok=True)
            filepath = os.path.join('app/static/uploads/avatars', filename)
            avatar_file.save(filepath)
            student.avatar = f'/static/uploads/avatars/{filename}'

        db.session.commit()
        flash('Профиль обновлён!', 'success')
        return redirect(url_for('main.student_settings'))

    profile_form.full_name.data = student.full_name
    profile_form.group_name.data = student.group_name
    profile_form.course.data = str(student.course)
    profile_form.phone.data = student.phone
    profile_form.telegram.data = student.telegram
    profile_form.bio.data = student.bio

    return render_template('cabinet/student_settings.html', breadcrumb_title='Настройки',
                           student=student, profile_form=profile_form, password_form=password_form)


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

@bp.route('/cabinet/teacher/students-works')
@login_required
def teacher_students_works():
    if current_user.role != 'teacher':
        abort(403)
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    works = Document.query.join(Discipline).filter(Discipline.teacher_id == teacher.id).all()
    return render_template('cabinet/teacher/students_works.html', breadcrumb_title='Работы студентов', teacher=teacher, works=works)


@bp.route('/cabinet/teacher/grades')
@login_required
def teacher_grades():
    if current_user.role != 'teacher':
        abort(403)
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    students = Student.query.all()
    disciplines = Discipline.query.filter_by(teacher_id=teacher.id).all()
    grades = Grade.query.join(Discipline).filter(Discipline.teacher_id == teacher.id).all()
    return render_template('cabinet/teacher/grades.html', breadcrumb_title='Выставление оценок',
                           teacher=teacher, students=students, disciplines=disciplines, grades=grades)


@bp.route('/cabinet/teacher/add-grade', methods=['POST'])
@login_required
def teacher_add_grade():
    if current_user.role != 'teacher':
        abort(403)
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()

    student_id = request.form.get('student_id')
    discipline_id = request.form.get('discipline_id')
    grade_value = request.form.get('grade_value')
    grade_type = request.form.get('grade_type')

    if student_id and discipline_id and grade_value:
        grade = Grade(
            student_id=student_id,
            discipline_id=discipline_id,
            grade_value=int(grade_value),
            grade_type=grade_type,
            teacher_id=teacher.id
        )
        db.session.add(grade)
        db.session.commit()
        flash('Оценка выставлена!', 'success')

    return redirect(url_for('main.teacher_grades'))

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