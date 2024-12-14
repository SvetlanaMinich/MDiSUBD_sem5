from db_service import DataBaseService

db = DataBaseService()

class ClubCard:
    @staticmethod
    def create_clubcard(hours,
                        field_id):
        comm = f'''insert into clubcard
        (hours, field_id)
        values
        ({hours}, {field_id});'''
        response = db.run(comm, fetch=False)
        return response
    
    @staticmethod
    def delete_clubcard(clubcard_id):
        comm = f'''drop from clubcard
        where cliencard_id={clubcard_id};'''
        response = db.run(comm, fetch=False)
        return response
    
    @staticmethod
    def get_clubcard(clubcard_id):
        comm = f'''select * from clubcard
        where clubcard_id={clubcard_id};'''
        response = db.run(comm, fetch=True)
        return response
    
    @staticmethod
    def get_all_clubcards():
        comm = f'''select * from clubcard;'''
        response = db.run(comm, fetch=True)
        return response
    
    @staticmethod
    def get_clubcards_by_field_id(field_id):
        comm = f'''select * from clubcard
        where field_id={field_id};'''
        response = db.run(comm, fetch=True)
        return response
    
    @staticmethod
    def get_clubcards_sorted_by_time_asc():
        comm = f'''select * from clubcard
        sort by hours asc;'''
        response = db.run(comm, fetch=True)
        return response
    
    @staticmethod
    def get_clubcards_sorted_by_time_desc():
        comm = f'''select * from clubcard
        sort by hours desc;'''
        response = db.run(comm, fetch=True)
        return response