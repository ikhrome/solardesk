import functools, sqlite3

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from solar.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/register', methods=('GET', 'POST'))
def register():
    from .forms.login import RegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        db = get_db()
        error = None

        if db.execute(
                'SELECT id FROM user WHERE username = ?', (form.username.data,)
        ).fetchone() is not None:
            error = 'Пользователь {} уже существует!.'.format(form.username.data)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password, email, phone_number, first_name, middle_name, last_name)'
                'VALUES (?, ?, ?, ?, ?, ?, ?)',
                (
                    form.username.data,
                    generate_password_hash(form.password.data),
                    form.email.data,
                    form.phone_number.data,
                    form.first_name.data,
                    form.middle_name.data,
                    form.last_name.data,
                )
            )
            db.commit()
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    from .forms.login import LoginForm
    form = LoginForm()
    if form.validate_on_submit():
        db = get_db()
        error = None

        user = db.execute(
            'SELECT id, username, active, password FROM user WHERE username = ?', (form.username.data,)
        ).fetchone()

        if user is None:
            error = 'Такого пользователя не существует'
        elif not check_password_hash(user['password'], form.password.data):
            error = 'Неправильный пароль'
        elif user['active'] == 0:
            error = 'Данная учетная запись не была активирована администратором системы. Подождите, ' \
                    'пока администратор активирует учетную запись '

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('tickets.index'))

        flash(error)
    return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('tickets.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


def for_admin(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user:
            flash('Необходима авторизация!')
            return redirect(url_for('auth.login'))
        else:
            if not g.user['position'] == 'admin':
                flash('Эта функция доступна только для администраторов системы!')
                return redirect(url_for('tickets.index'))

        return view(**kwargs)

    return wrapped_view
