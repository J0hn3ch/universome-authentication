import sqlite3
import flask_login

class User(flask_login.UserMixin):
    def __init__(self, username, active=True):
        self.id = username # https://stackoverflow.com/questions/37472870/login-user-fails-to-get-user-id 
        self.username = username
        self.active = active

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