from app.main import bp

@bp.route('/')
def index():
    return '<h1>Портал кафедры ИТ Московского Университета им. Витте</h1><p>Добро пожаловать!</p>'

@bp.route('/about')
def about():
    return '<h1>О кафедре</h1><p>Страница в разработке</p>'