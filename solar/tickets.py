from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from solar.auth import login_required
from solar.db import get_db

bp = Blueprint('tickets', __name__, url_prefix='/tickets')

@bp.route('/')
def index():
    inactive_users = get_db().execute(
        'SELECT id,username FROM user WHERE active=0'
    ).fetchall()
    return render_template('tickets/index.html', inactive_users=inactive_users)

@bp.route('/submit')
@login_required
def submit():
    return render_template('tickets/submit.html')