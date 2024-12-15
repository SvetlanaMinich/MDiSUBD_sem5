from db_service import DataBaseService

db = DataBaseService()

class Admin:
    @staticmethod
    def create_admin(name,
                     login,
                     password):
        comm = f'''insert into adminacc
        (nickname, login, password)
        values
        ('{name}', '{login}', '{password}');'''
        response = db.run(comm, fetch=False)
        return response
    
    @staticmethod
    def get_admin(login,
                   password):
        comm = f'''select * from adminacc
        where login='{login}' and admin_password='{password}';'''
        response = db.run(comm, fetch=True)
        return response
    
    @staticmethod
    def get_admin_by_id(adminacc_id):
        comm = f'''select * from adminacc
        where adminacc_id={adminacc_id};'''
        response = db.run(comm, fetch=True)
        return response