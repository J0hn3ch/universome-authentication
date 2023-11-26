import sqlite3
from flask_login import UserMixin

class User(UserMixin):
    __tablename__ = "user"

    def __init__(self, username, password):
        self.id = username # https://stackoverflow.com/questions/37472870/login-user-fails-to-get-user-id 
        self.username = username
        self.password = password
    
    def __repr__(self):
        return '<User %r>' % self.username

    def is_active(self):
         return self.is_active()

    def is_anonymous(self):
         return False

    def is_authenticated(self):
         return self.authenticated

    def is_active(self):
         return True

    def get_id(self):
         return self.id

def getUser():
    conn = sqlite3.connect('/var/www/flask/login.db')
    curs = conn.cursor()
    curs.execute("SELECT * FROM login where email = (?)", [form.email.data])
    user = list(curs.fetchone())
    Us = load_user(user[0])
    if form.email.data == Us.email and form.password.data == Us.password:
        login_user(Us, remember=form.remember.data)
        Umail = list({form.email.data})[0].split('@')[0]
        flash('Logged in successfully '+Umail)
        return True
    else:
        flash('Login Unsuccessfull.')
        return False


def insertUser(username,password):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,password))
    con.commit()
    con.close()

def retrieveUsers():
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT username, password FROM users")
	users = cur.fetchall()
	con.close()
	return users