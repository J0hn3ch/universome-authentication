import sqlite3
from flask_login import UserMixin
from authentication.db import get_db

class User(UserMixin):
     __tablename__ = "user"

     def __init__(self, id, username=None, password=None):
          self.id = id # https://stackoverflow.com/questions/37472870/login-user-fails-to-get-user-id 
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

     @staticmethod
     def get_user(username, hashed_password):
          print("UserModel: get_user")
          user = None
          try:
               db = get_db()
               if db:
                    print("UserModel: Database connection established!")
               cur = db.cursor()
               if cur:
                    print("UserModel: Cursor obtained!")
               
               # Query execution
               query = "SELECT * FROM user WHERE username=(?) AND password=(?)"
               result = cur.execute(query, (username, hashed_password))
               if cur:
                    print("UserModel: Query executed!")
               record = result.fetchone()

               cur.close()
               #db.close()
          except Exception as e:
               raise e
          else:
               print(record)
               if record is None:
                    print("UserModel: No user found")
                    user = None
               else:
                    print("UserModel: User found!")
                    user = User(int(record[0]), record[1], record[2])
               return user
          
     @staticmethod
     def get_user_by_id(user_id):
          print("UserModel: get_user_by_id")
          user = None
          try:
               db = get_db()
               cur = db.cursor()   
          except Exception as e:
               raise e
          else:
               query = "SELECT * FROM user WHERE id=(?)"
               results = cur.execute(query, str(user_id))
               record = results.fetchone()
               
               if record is not None:
                    user = User(int(record[0]), record[1], record[2])
               
               cur.close()
               #db.close()
               return user

     @staticmethod
     def insert_user(username, email, password):
          user = None

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