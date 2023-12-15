from flask import (Blueprint, render_template)
from flask_login import login_required, current_user

main = Blueprint('main', __name__, url_prefix='/')

# Index page
@main.route('/', methods=["GET", "POST"], strict_slashes=False)
def index():
    return render_template('page/index.html', title="Home")

# About Us page
@main.route('/about-us', methods=["GET"], strict_slashes=False)
def about_us():
    return render_template('page/about-us.html', title="About Us")

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/dashboard.html', title="Dashboard", username=current_user.username)

@main.route('/settings')
@login_required
def settings():
    return 'Settings'