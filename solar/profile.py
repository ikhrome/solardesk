import functools, sqlite3

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from solar.db import get_db
from solar.auth import login_required

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/edit')
@login_required
def edit():
    return render_template('profile/edit.html')