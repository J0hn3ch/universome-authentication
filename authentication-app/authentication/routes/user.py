from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)

from flask_login import login_user, login_required, logout_user

usr = Blueprint('user', __name__, url_prefix='/auth')

@usr.route('/user/<id>')
@login_required
def list_member(id):
    return render_template('page.html', name=name)
