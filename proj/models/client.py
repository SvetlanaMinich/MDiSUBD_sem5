from db_service import DataBaseService

db = DataBaseService()

class Client:
    @staticmethod
    def create_client(name,
                      surname,
                      birth_date,
                      login,
                      password):
        comm = f'''call add_client(
        '{name}', '{surname}', '{birth_date}', '{login}', '{password}');'''
        response = db.run(comm, fetch=False)
        return response
    
    @staticmethod
    def update_client_name(client_id,
                           name):
        comm = f'''update client
        set client_name='{name}'
        where client_id={client_id};'''
        response = db.run(comm, fetch=False)
        return response
    
    @staticmethod
    def update_client_surname(client_id,
                              surname):
        comm = f'''update client
        set client_surname='{surname}'
        where client_id={client_id};'''
        response = db.run(comm, fetch=False)
        return response
    
    @staticmethod
    def update_client_birth_date(client_id,
                                 birth_date):
        comm = f'''update client
        set birth_date='{birth_date}'
        where client_id={client_id};'''
        response = db.run(comm, fetch=False)
        return response
    
    @staticmethod
    def update_client_login(client_id,
                            login):
        comm = f'''update clientcredentials
        set client_login='{login}'
        where client_id={client_id};'''
        response = db.run(comm, fetch=False)
        return response
    
    @staticmethod
    def update_client_password(client_id,
                               password):
        comm = f'''update clientcredentials
        set client_password='{password}'
        where client_id={client_id};'''
        response = db.run(comm, fetch=False)
        return response
    
    @staticmethod
    def create_client_payment(client_id,
                              card_iban):
        comm = f'''insert into clientpaymentcredentials
        (client_id, card_iban)
        values
        ({client_id}, '{card_iban}');'''
        response = db.run(comm, fetch=False)
        return response
    
    @staticmethod
    def remove_client_payment(client_id,
                              card_iban):
        comm = f'''drop from clientpaymentcredentials
        where client_id={client_id} and card_iban='{card_iban}';'''
        response = db.run(comm, fetch=False)
        return response
    
    @staticmethod
    def delete_client(client_id):
        comm = f'''drop from client
        where client_id={client_id};'''
        response = db.run(comm, fetch=False)
        return response
    
    @staticmethod
    def get_client(login,
                   password):
        comm = f'''call get_client_by_login_and_password('{login}', '{password}', null);'''
        response = db.run(comm, fetch=True)
        if isinstance(response, list):
            cl_id = response[0][0]
            comm = f'''select * from client
            where client_id={cl_id};'''
            response = db.run(comm, fetch=True)
        return response
    
    @staticmethod
    def get_all_clients():
        comm = f'''select * from client;'''
        response = db.run(comm, fetch=False)
        return response