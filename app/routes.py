from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify, abort
from .models import User, Profile, ActivityLog, News
from . import db
from .forms import RegisterForm, LoginForm, ProfileForm, NewsForm
from flask_login import login_user, logout_user, login_required, current_user
from .utils import save_avatar
import psutil
from functools import wraps


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    news_list = News.query.order_by(News.created_at.desc()).all()
    return render_template('index.html', news_list=news_list)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first():
            flash('Користувач із таким іменем або email вже існує', 'warning')
            return redirect(url_for('main.register'))
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        profile = Profile(user_id=user.id)
        db.session.add(profile)
        db.session.commit()
        # лог активності
        log = ActivityLog(user_id=user.id, action='register')
        db.session.add(log)
        db.session.commit()
        flash('Реєстрація успішна. Увійдіть у систему.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            log = ActivityLog(user_id=user.id, action='login')
            db.session.add(log)
            db.session.commit()
            flash('Успішний вхід', 'success')
            return redirect(url_for('main.dashboard'))
        flash('Невірні дані', 'danger')
    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    log = ActivityLog(user_id=current_user.id, action='logout')
    db.session.add(log)
    db.session.commit()
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    profile = current_user.profile
    if form.validate_on_submit():
        if form.full_name.data:
            profile.full_name = form.full_name.data
        profile.bio = form.bio.data
        if form.avatar.data:
            avatar_path = save_avatar(form.avatar.data, f'user{current_user.id}')
            if avatar_path:
                profile.avatar = avatar_path
        db.session.commit()
        log = ActivityLog(user_id=current_user.id, action='update_profile')
        db.session.add(log)
        db.session.commit()
        flash('Профіль оновлено', 'success')
        return redirect(url_for('main.profile'))
    return render_template('profile.html', form=form, profile=profile)


@bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        flash('Недостатньо прав', 'danger')
        return redirect(url_for('main.index'))
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('dashboard.html', users=users)


@bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@bp.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


# endpoint для збору простих метрик (зручно для тестів)
@bp.route('/metrics')
def metrics():
    p = psutil.Process()
    mem = p.memory_info().rss / 1024 / 1024  # MB
    cpu = p.cpu_percent(interval=0.1)
    return jsonify({
        'cpu_percent': cpu,
        'memory_mb': round(mem, 2)
    })


@bp.route('/admin/add-news', methods=['GET', 'POST'])
@login_required
@admin_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        new_article = News(
            title=form.title.data,
            summary=form.summary.data,
            content=form.content.data,
            image_url=form.image_url.data,
            user_id=current_user.id
        )
        db.session.add(new_article)
        db.session.commit()
        log = ActivityLog(user_id=current_user.id, action='add_news')
        db.session.add(log)
        db.session.commit()
        flash('Новину успішно додано!', 'success')
        return redirect(url_for('main.index'))
    return render_template('add_news.html', form=form)


@bp.route('/news/<int:news_id>')
def news_detail(news_id):
    news = News.query.get_or_404(news_id)
    return render_template('news_detail.html', news=news)