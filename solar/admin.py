import functools, sqlite3

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from solar.db import get_db
from solar.auth import for_admin

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
@for_admin
def index():
    return render_template('admin/index.html')


@bp.route('/users')
@for_admin
def users():
    users = get_db().execute(
        'SELECT u.id, u.username, u.email, u.first_name, '
        'u.last_name, u.middle_name, f.title '
        'FROM user AS u LEFT JOIN firms AS f ON u.firm_id = f.id '
        'WHERE u.active=1 ORDER BY username ASC'
    ).fetchall()
    firms = get_db().execute(
        'SELECT * FROM firms ORDER BY title ASC'
    ).fetchall()
    return render_template('admin/users.html', users=users, firms=firms)


@bp.route('/activate', methods=('POST',))
@for_admin
def activate():
    error = None
    user_id = request.form['userid']
    come_from = request.form['from']

    if user_id is None:
        error = 'Не указан ID пользователя!'

    if error is None:
        db = get_db()
        db.execute(
            'UPDATE user SET active = 1'
            ' WHERE id = ?',
            (user_id,)
        )
        db.commit()

    message = None
    if error is not None:
        message = 'Произошла ошибка: ' + error
    else:
        message = 'Пользователь активирован!'
    flash(message)

    return redirect(url_for(come_from))


@bp.route('/test')
@for_admin
def test():
    return 'Yes, you are admin!'
