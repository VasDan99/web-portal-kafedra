# Редактирование профиля студента
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

        # Обработка загрузки фото
        if form.avatar.data:
            avatar_file = form.avatar.data
            filename = f'user_{current_user.id}.jpg'
            filepath = os.path.join('app/static/uploads/avatars', filename)
            avatar_file.save(filepath)
            student.avatar = f'/static/uploads/avatars/{filename}'

        db.session.commit()
        flash('Профиль обновлён!', 'success')
        return redirect(url_for('main.student_profile'))

    # Заполняем форму текущими данными
    form.full_name.data = student.full_name
    form.group_name.data = student.group_name
    form.course.data = str(student.course)
    form.phone.data = student.phone
    form.telegram.data = student.telegram
    form.bio.data = student.bio

    return render_template('cabinet/student_profile_edit.html', breadcrumb_title='Редактирование профиля', form=form,
                           student=student)


# Загрузка работ студента
@bp.route('/cabinet/student/works/upload', methods=['POST'])
@login_required
def student_works_upload():
    if current_user.role != 'student':
        abort(403)

    file = request.files.get('file')
    title = request.form.get('title')

    if file and title:
        filename = f'work_{current_user.id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        filepath = os.path.join('app/static/uploads/works', filename)
        file.save(filepath)

        # Сохраняем информацию о работе в БД
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


# Задать вопрос преподавателю
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
            # Сохраняем в обратную связь с пометкой для преподавателя
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

    return render_template('cabinet/ask_teacher.html', breadcrumb_title='Задать вопрос', teacher=teacher,
                           student=student)