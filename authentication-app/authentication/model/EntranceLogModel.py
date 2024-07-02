from authentication.db import get_db
import json

class EntranceLog():
     __tablename__ = "entrance"

     def __init__(self, id, entrance_date, full_name, card_id, authorized):
          self.id = id
          self.entrance_date = entrance_date
          self.full_name = full_name
          self.card_id = card_id
          self.authorized = authorized

     def __repr__(self):
          return f"EntranceLog('{self.entrance_date}', '{self.full_name}', {self.card_id}, '{self.authorized}')"
     
     @staticmethod
     def get_entrances_log():
          try:
               db = get_db()
               cur = db.cursor()
          except Exception as e:
               raise e
          else:
               query = "SELECT * FROM entrance ORDER BY entrance_date DESC"
               records = cur.execute(query).fetchall()

               # Get all the records and make it a list of Member object to return
               entrances = list()
               for record in records:
                    entrance = EntranceLog(
                         id=int(record['id']),
                         entrance_date=record['entrance_date'],
                         full_name=record['full_name'],
                         card_id=record['card_id'],
                         authorized=bool(record['authorized']),
                    )
                    entrances.append(entrance)

               cur.close()
               return entrances
     
     @staticmethod
     def create_entrance(entrance_date, full_name, card_id, authorized):
          try:
               db = get_db()
               print("Connection established!")
               cur = db.cursor()   
               print("Cursor opened")
          except Exception as e:
               raise e
          else:            
               query = "INSERT INTO entrance(entrance_date, full_name, card_id, authorized) VALUES(?,?,?,?)"
               cur.execute(query, (entrance_date, full_name, card_id, str(authorized).upper()))
               db.commit()
               #records = results.fetchall()
               cur.close()
               return "Entrance registered" #records

     # - https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable  
     def to_json(self):
          return self.__dict__
          return json.dumps(self, ensure_ascii=True, default=lambda o: o.__dict__)