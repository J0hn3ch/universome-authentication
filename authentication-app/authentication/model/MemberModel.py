from authentication.db import get_db, query_db
import time
import json

class Member():
     __tablename__ = "member"

     def __init__(self, full_name, role, student_id, authorized, id=None, created=None, card_id=None):
          self.id = id # https://stackoverflow.com/questions/37472870/login-user-fails-to-get-user-id 
          self.full_name = full_name
          self.role = role
          self.student_id = student_id
          self.created = created
          self.authorized = authorized

     def get_id(self):
          return self.id
     
     def _check_attributes(self):
          validation_flag = (self.full_name is not None) \
               and (self.member_role is not None) \
               and (self.student_id is not None) \
               and (self.authorized is not None)
          return validation_flag
     
     @staticmethod
     def get_member(member_id=None, chip_id=None):
          print("MemberModel: get_member, id = ", member_id, type(member_id))
          try:
               db = get_db()
               cur = db.cursor()
          except Exception as e:
               raise e
          else:
               if (member_id is None and chip_id is None):
                    query = "SELECT * FROM member" #+ "" if (id is None) else "WHERE id=(?)"
                    records = cur.execute(query).fetchall()
               elif (chip_id is not None):
                    query = "SELECT * FROM member WHERE chip_id=(?)"
                    records = cur.execute(query, [str(chip_id)]).fetchone()
               else:
                    query = "SELECT * FROM member WHERE id=(?)"
                    print("MemberModel: query = ", str(member_id), type(str(member_id)))
                    records = cur.execute(query, str(member_id)).fetchall()

               # Get all the records and make it a list of Member object to return
               members = list()
               for record in records:
                    print("MemberModel: record[\'id\'] = ", record['id'], type(record['id']))
                    member = Member(
                         id=int(record['id']),
                         full_name=record['full_name'],
                         role=record['member_role'],
                         student_id=record['student_id'],
                         created=str(record['created']),
                         authorized=bool(record['authorized']),
                         card_id=record['card_id']
                    )
                    members.append(member)
                    print(member.__dict__)

               cur.close()
               return members
     
     def create_member(self):
          try:
               db = get_db()
               print("Connection established!")
               cur = db.cursor()   
               print("Cursor opened")
          except Exception as e:
               raise e
          else:
               if (self._check_attributes()):
                    query = "INSERT INTO member VALUES ('"+ self.full_name + "', '" + self.member_role + "', '" + self.student_id + "', CURRENT_TIMESTAMP, " + str(self.authorized).upper() + ", '" + self.chip_id + "');"
                    #results = cur.execute(query)

               #records = results.fetchall()
               
               cur.close()
               return query #records

     # - https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable  
     def to_json(self):
          return self.__dict__
          return json.dumps(self, ensure_ascii=True, default=lambda o: o.__dict__)