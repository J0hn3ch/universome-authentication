from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)

from flask_login import login_user, login_required, logout_user

lgn = Blueprint('auth', __name__, url_prefix='/auth')

@mbr.route('/members/<name>')
@login_required
def list_member(name):
    return render_template('page.html', name=name)