import psycopg2
import datetime

class queries:
    def __init__(self):
        self.connection = psycopg2.connect("dbname=app user=postgres password=postgres")
        self.cursor = self.connection.cursor()

    def add_field(self, 
                  field_name:str,
                  field_location:str,
                  price_per_hour:float):
        sql = f'''insert into field
        (field_name, field_location, price_per_hour) 
        values
        ({field_name}, {field_location}, {price_per_hour})'''
        self.cursor.execute(sql)
        self.connection.commit()

    def get_field_by_id(self,
                        field_id:int):
        sql = f'''select * from field
        where field_id = {field_id}'''
        self.cursor.execute(sql)
        field = self.cursor.fetchone()
        return field

    def get_field_by_name(self,
                          field_name:str):
        sql = f'''select * from field
        where field_name = {field_name}'''
        self.cursor.execute(sql)
        field = self.cursor.fetchone()
        return field

    def update_field(self,
                     field_id:int,
                     field_name:str,
                     field_location:str,
                     price_per_hour:float):
        sql = f'''select rating from review
        where field_id = {field_id}'''
        self.cursor.execute(sql)
        ratings = self.cursor.fetchall()
        rating = 5 if not ratings else sum([r[0] for r in ratings])//len(ratings)

        sql = f'''update field
        set field_name = {field_name}, field_location = {field_location}, price_per_hour = {price_per_hour}, rating = {rating}
        where field_id = {field_id}'''
        self.cursor.execute(sql)
        self.connection.commit()
    
    def delete_field(self,
                     field_id:int):
        sql = f'''delete from field
        where field_id = {field_id}'''
        self.cursor.execute(sql)
        self.connection.commit()

    
    def add_admin(self, 
                  nickname:str,
                  login:str,
                  password:str):
        sql = f'''insert into adminacc
        (nickname, login, admin_password) 
        values
        ({nickname}, {login}, {password})
        returning adminacc_id'''
        self.cursor.execute(sql)
        admin_id = self.cursor.fetchone()[0]
        self.connection.commit()
        return admin_id
    
    def get_admin_by_id(self,
                        admin_id:int):
        sql = f'''select * from adminacc
        where adminacc_id = {admin_id}'''
        self.cursor.execute(sql)
        admin = self.cursor.fetchone()
        return admin

    def update_admin(self,
                     admin_id:int,
                     nickname:str,
                     login:str,
                     password: str):
        sql = f'''update adminacc
        set nickname = '{nickname}', login = '{login}', admin_password = '{password}'
        where admin_id = {admin_id}'''
        self.cursor.execute(sql)
        self.connection.commit()

    def delete_admin(self,
                     admin_id:int):
        sql = f'''delete from adminacc
        where admin_id = {admin_id}'''
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
        self.cursor.execute(sql)
        client_id = self.cursor.fetchone()[0]

        sql = f'''insert into clientcredentials
        (client_id, client_login, client_password)
        values
        ({client_id}, {login}, {password})'''
        self.cursor.execute(sql)

        self.connection.commit()  
        return client_id
    
    def get_client_by_id(self,
                         client_id:int):
        sql = f'''select * from client
        where client_id = {client_id}'''
        self.cursor.execute(sql)
        client = self.cursor.fetchone()
        return client

    def update_client_info(self, 
                    client_id:int,
                    name:str,
                    surname:str,
                    birth_date:datetime.datetime):
        sql = f'''update client
        set client_name = {name}, client_surname = {surname}, birth_date = {birth_date} 
        where client_id = {client_id}'''
        self.cursor.execute(sql)
        self.connection.commit() 

    def update_clientCredentials(self,
                                 client_id:int,
                                 login:str,
                                 password:str):
        sql = f'''update clientCredentials
        set client_login = {login}, client_password = {password}
        where client_id = {client_id}'''
        self.cursor.execute(sql)
        self.connection.commit()

    def delete_client(self,
                      client_id:int):
        sql = f'''delete from client
        where client_id = {client_id}'''
        self.cursor.execute(sql)
        self.connection.commit()


    def add_clientPaymentCredentials(self,
                                     client_id:int,
                                     card_iban:str):
        sql = f'''insert into clientpaymentcredentials
        (client_id, card_iban)
        values
        ({client_id}, {card_iban})'''
        self.cursor.execute(sql)
        self.connection.commit()

    def get_clientPaymentCredentials_by_clientId(self,
                                                 client_id:int):
        sql = f'''select * from clientpaymentcredentials
        where client_id = {client_id}'''
        self.cursor.execute(sql)
        clientpayment = self.cursor.fetchone()
        return clientpayment

    def update_clientPaymentCredentials(self,
                                        client_id:int,
                                        card_iban:str):
        sql = f'''update clientpaymentcredentials
        set card_iban = '{card_iban}'
        where client_id = {client_id}'''
        self.cursor.execute(sql)
        self.connection.commit()

    def delete_clientPaymentCredentials(self,
                                        client_id:int):
        sql = f'''delete from clientpaymentcredentials
        where client_id = {client_id}'''
        self.cursor.execute(sql)
        self.connection.commit()


    def add_clubcard(self,
                     hours:int,
                     field_id:int):
        sql = f'''insert into clubcard
        (hours, field_id)
        values
        ({hours}, {field_id})
        returning clubcard_id'''
        self.cursor.execute(sql)
        clubcard_id = self.cursor.fetchone()[0]
        self.connection.commit()
        return clubcard_id

    def get_clubCard_by_id(self,
                           clubcard_id:int):
        sql = f'''select * from clubcard
        where clubcard_id = {clubcard_id}'''
        self.cursor.execute(sql)
        clubcard = self.cursor.fetchone()
        return clubcard

    def update_clubcard(self,
                        clubcard_id:int,
                        hours:int,
                        field_id:int):
        sql = f'''update clubcard
        set hours = {hours}, field_id = {field_id}
        where clubcard_id = {clubcard_id}'''
        self.cursor.execute(sql)
        self.connection.commit()

    def delete_clubcard(self,
                        clubcard_id:int):
        sql = f'''delete from clubcard
        where clubcard_id = {clubcard_id}'''
        self.cursor.execute(sql)
        self.connection.commit()


    def add_review(self,
                   client_id:int,
                   field_id:int,
                   rating:int,
                   text:str):
        sql = f'''insert into review
        (client_id, rating, text, field_id)
        values
        ({client_id}, {rating}, {text}, {field_id})'''
        self.cursor.execute(sql)
        self.connection.commit()

    def get_reviews_by_fieldId(self,
                              field_id:int):
        sql = f'''select * from review
        where field_id = {field_id}'''
        self.cursor.execute(sql)
        reviews = self.cursor.fetchmany()
        return reviews
    
    def get_reviews_by_clientId(self,
                                client_id:int):
        sql = f'''select * from review
        where client_id = {client_id}'''
        self.cursor.execute(sql)
        reviews = self.cursor.fetchmany()
        return reviews

    def update_review(self,
                      review_id:int,
                      rating: int,
                      text:str):
        sql = f'''update review
        set rating = {rating}, text = '{text}'
        where review_id = {review_id}'''
        self.cursor.execute(sql)
        self.connection.commit()

    def delete_review(self,
                      review_id:int):
        sql = f'''delete from review
        where review_id = {review_id}'''
        self.cursor.execute(sql)
        self.connection.commit()


    def add_schedule(self,
                     field_id:int,
                     time_from:datetime.datetime,
                     time_to:datetime.datetime):
        sql = f'''insert into schedule
        (field_id, time_from, time_to)
        values
        ({field_id}, {time_from}, {time_to})'''
        self.cursor.execute(sql)
        self.connection.commit()

    def get_schedule_by_fieldId(self,
                                field_id:int):
        sql = f'''select * from schedule
        where field_id = {field_id}'''
        self.cursor.execute(sql)
        schedules = self.cursor.fetchmany()
        return schedules

    def update_schedule(self,
                        schedule_id:int,
                        time_from:datetime.datetime,
                        time_to:datetime.datetime):
        sql = f'''update schedule
        set time_from = '{time_from}', time_to = '{time_to}'
        where schedule_id = {schedule_id}'''
        self.cursor.execute(sql)
        self.connection.commit()

    def delete_schedule(self,
                        schedule_id:int):
        sql = f'''delete from schedule
        where schedule_id = {schedule_id}'''
        self.cursor.execute(sql)
        self.connection.commit()


    def add_reservation(self,
                        client_id:int,
                        schedule_id:int):
        sql = f'''insert into reservation
        (client_id, schedule_id)
        values
        ({client_id}, {schedule_id})'''
        self.cursor.execute(sql)

        sql = f'''update schedule
        set is_available = false
        where schedule_id = {schedule_id}'''
        self.cursor.execute(sql)

        self.connection.commit()

    def get_reservation_by_clientId(self,
                                    client_id:int):
        sql = f'''select * from reservation
        where client_id = {client_id}'''
        self.cursor.execute(sql)
        reservations = self.cursor.fetchmany()
        return reservations
    
    def delete_reservation(self,
                           reservation_id:int, 
                           schedule_id:int):
        sql = f'''delete from reservation
        where reservation_id = {reservation_id}'''
        self.cursor.execute(sql)

        sql = f'''update schedule
        set is_available = true
        where schedule_id = {schedule_id}'''
        self.cursor.execute(sql)

        self.connection.commit()
        