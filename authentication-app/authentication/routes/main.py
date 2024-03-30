from flask import (Blueprint, render_template, current_app, request)
from flask_login import login_required, current_user
from flask_socketio import SocketIO, emit
from authentication.controller.MemberController import MemberController
from authentication.model.form import RfidValidation
from serial import Serial
import threading
import time

main = Blueprint('main', __name__, url_prefix='/')
#socketio = SocketIO(current_app, cors_allowed_origins='*')

# Index page
@main.route('/', methods=["GET", "POST"], strict_slashes=False)
@main.route('/home', methods=["GET", "POST"], strict_slashes=False)
@main.route('/index', methods=["GET", "POST"], strict_slashes=False)
def index():
    form = RfidValidation()
    return render_template('page/index.html', title="Home", form=form)

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
    with Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1) as ser:
        ser_name = ser.name
        app.logger.info('==== Start listener at %s ====', ser_name)
        
        if not ser.is_open:
            ser.open()
        
        print("Serial name", ser_name, "is open? ", ser.is_open)
        try:
            ser.reset_input_buffer()
            while True:
                time.sleep(0.01)
                if ser.in_waiting > 0:
                    line = ser.readline() # Read raw data from the stream
                    message = line.decode('utf-8') # Convert the binary string to a normal string
                
                    # Remove the trailing newline character
                    # message = ser.read(5).decode('utf-8')
                    #message = ser.readline().decode().rstrip()
                    app.logger.info('[RFID UID]: %s', message)
                    print(f'[RFID UID]: {message}')
        except KeyboardInterrupt:
            app.logger.info('Close serial communication')
        finally:
            ser.close()

@main.route('/serial')
def serial():
    with Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1) as ser:
        ser_name = ser.name
        current_app.logger.info('==== Start listener at %s ====', ser_name)
        
    if not ser.is_open:
        ser.open()
    
    print("Serial name", ser_name, "is open? ", ser.is_open)
    try:
        ser.reset_input_buffer()
        while True:
            time.sleep(0.01)
            if ser.in_waiting > 0:
                line = ser.readline() # Read raw data from the stream
                message = line.decode('utf-8') # Convert the binary string to a normal string
            
                # Remove the trailing newline character
                # message = ser.read(5).decode('utf-8')
                #message = ser.readline().decode().rstrip()
                current_app.logger.info('[RFID UID]: %s', message)
                print(f'[RFID UID]: {message}')
    except KeyboardInterrupt:
        current_app.logger.info('Close serial communication')
    finally:
        ser.close()
    
    #threading.Thread(target=background_thread()).start()
    #x = threading.Thread(target=background_thread, args=(current_app), daemon=True)
    #x.start()
    #background_thread(current_app)
    return render_template('page/serial.html', title="Serial")

@main.route('/settings')
@login_required
def settings():
    return 'Settings'