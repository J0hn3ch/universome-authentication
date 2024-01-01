from flask import (Blueprint, render_template)
from flask_login import login_required, current_user
from authentication.controller.MemberController import MemberController
from serial import Serial

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
    member_controller = MemberController()
    members = member_controller.getMember()
    return render_template('dashboard/dashboard.html', title="Dashboard", username=current_user.username, members=members)

@main.route('/serial')
def serial():
    #ser = Serial('/dev/ttyS1', 115200)  # open serial port
    with Serial('/dev/ttyS1', 115200, timeout=3) as ser:
        ser_name = ser.name
        if not ser.is_open:
            ser.open()
        print("Serial name, is open? ", ser.is_open)
        ser.write(b'CIAO')     # write a string
        ser.close()
        ser.open()
        message = ser.read(5).decode('utf-8')
        ser.close()
    print("Message: ", message)
    return render_template('page/serial.html', title="Serial", ser_name=ser_name, message=message)

@main.route('/settings')
@login_required
def settings():
    return 'Settings'