from flask import (Blueprint, render_template, current_app, request)
from flask_login import login_required, current_user
from flask_socketio import SocketIO, emit
from authentication.controller.MemberController import MemberController
from serial import Serial
import threading

main = Blueprint('main', __name__, url_prefix='/')
#socketio = SocketIO(current_app, cors_allowed_origins='*')

# Index page
@main.route('/', methods=["GET", "POST"], strict_slashes=False)
@main.route('/index', methods=["GET", "POST"], strict_slashes=False)
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

"""
Thread functions
"""
thread = None
thread_lock = threading.Lock()

def background_thread(app):
    with Serial(port='/dev/ttyS1', baudrate=115200, timeout=1) as ser:
        ser_name = ser.name
        app.logger.info('==== Start listener at %s ====', ser_name)
        
        if not ser.is_open:
            ser.open()
        
        print("Serial name", ser_name, "is open? ", ser.is_open)
        try:
            while True:
                # Read raw data from the stream
                # Convert the binary string to a normal string
                # Remove the trailing newline character
                # message = ser.read(5).decode('utf-8')
                message = ser.readline().decode().rstrip()
                print(f'Message: {message}')
        finally:
            ser.close()

@main.route('/serial')
def serial():
    #threading.Thread(target=background_thread()).start()
    x = threading.Thread(target=background_thread, args=(current_app), daemon=True)
    x. start()
    return render_template('page/serial.html', title="Serial")

@main.route('/settings')
@login_required
def settings():
    return 'Settings'