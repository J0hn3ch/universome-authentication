from authentication.model.UserModel import User

class UserController:
   def __init__(self, username, password):
      self.username = username
      self.password = password
   
   def login(self):
      user = User.get_user(self.username, self.password)
      print("UserController:" + str(type(user)))
      if isinstance(user, User):
         return user
      else:
         return None
   
   def getUserById(user_id):
      return User.get_user_by_id(user_id)

'''
@login_manager.user_loader
def load_user(user_id):
   conn = sqlite3.connect('/var/www/flask/login.db')
   curs = conn.cursor()
   curs.execute("SELECT * from login where id = (?)",[user_id])
   lu = curs.fetchone()
   if lu is None:
      return None
   else:
      return User(int(lu[0]), lu[1], lu[2])
'''