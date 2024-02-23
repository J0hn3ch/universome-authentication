from authentication.db import get_db
import time

class Member():
     __tablename__ = "member"

     def __init__(self, id, full_name, role, student_id, created, authorized):
          self.id = id # https://stackoverflow.com/questions/37472870/login-user-fails-to-get-user-id 
          self.full_name = full_name
          self.member_role = role
          self.student_id = student_id
          self.created = created
          self.authorized = authorized

     def get_id(self):
          return self.id
     
     @staticmethod
     def get_member(id=None, chip_id=None):
          print("MemberModel: get_member")
          try:
               db = get_db()
               print("Connection established!")
               cur = db.cursor()   
               print("Cursor opened")
          except Exception as e:
               raise e
          else:
               print(type(id))
               if (id is None and chip_id is None):
                    query = "SELECT * FROM member" #+ "" if (id is None) else "WHERE id=(?)"
                    results = cur.execute(query)
               elif (chip_id is not None):
                    query = "SELECT * FROM member WHERE chip_id=(?)"
                    results = cur.execute(query, [str(chip_id)])
               else:
                    query = "SELECT * FROM member WHERE id=(?)"
                    results = cur.execute(query, str(id))

               records = results.fetchall()
               
               cur.close()
               return records