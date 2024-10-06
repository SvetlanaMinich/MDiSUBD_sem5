import psycopg2
import datetime

class queries:
    def __init__(self):
        self.connection = psycopg2.connect("dbname=app user=postgres password=postgres")
        self.cursor = self.connection.cursor()

    def add_field(self, 
                  field_name:str,
                  field_location:str,
                  price_per_hour:float,
                  rating:int):
        sql = f'''insert into field
        (field_name, field_location, price_per_hour, rating) 
        values
        ({field_name}, {field_location}, {price_per_hour}, {rating})'''
        self.cursor.execute(sql)
        self.connection.commit()
    
    def add_admin(self, 
                  nickname:str,
                  login:str,
                  password:str):
        sql = f'''insert into adminacc
        (nickname, login, admin_password) 
        values
        ({nickname}, {login}, {password})'''
        self.cursor.execute(sql)
        self.connection.commit()

    def add_client(self, 
                  name:str,
                  surname:str,
                  birth_date:datetime.datetime,
                  login:str,
                  password:str):
        sql = f'''insert into client
        (client_name, client_surname, birth_date) 
        values
        ({name}, {surname}, {birth_date})
        returning client_id'''
        client_id = self.cursor.execute(sql)

        sql = f'''insert into clientcredentials
        (client_id, client_login, client_password)
        values
        ({client_id}, {login}, {password})'''
        self.cursor.execute(sql)
        
        self.connection.commit()    
        