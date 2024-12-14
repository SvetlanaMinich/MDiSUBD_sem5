from db_service import DataBaseService

db = DataBaseService()

class Field:
    @staticmethod
    def create_field(name,
                     location,
                     price_per_hour,
                     rating):
        comm = f'''insert into field (field_name, field_location, price_per_hour, rating)
        values ('{name}', '{location}', {price_per_hour}, {rating});'''
        response = db.run(comm, fetch=False)
        return response
    
    @staticmethod
    def update_field_name(field_id,
                          new_name):
        comm = f'''update field
        set field_name='{new_name}'
        where field_id={field_id};'''
        response = db.run(comm, fetch=False)
        return response
        
    
    @staticmethod
    def update_field_location(field_id,
                              new_location):
        comm = f'''update field
        set field_location='{new_location}'
        where field_id={field_id};'''
        response = db.run(comm, fetch=False)
        return response
    
    @staticmethod
    def update_field_price(field_id,
                           new_price):
        comm = f'''update field
        set price_per_hour={new_price}
        where field_id={field_id};'''
        response = db.run(comm, fetch=False)
        return response
    
    @staticmethod
    def delete_field(field_id):
        comm = f'''delete from field
        where field_id={field_id};'''
        response = db.run(comm, fetch=False)
        return response
    
    @staticmethod
    def get_all_fields():
        comm = f'''select * from field;'''
        response = db.run(comm, fetch=True)
        return response
    
    @staticmethod
    def get_fields_by_price(price_from=0, price_to=200):
        comm = f'''select * from field
        where price_per_hour >= {price_from} and price_per_hour <= {price_to};'''
        response = db.run(comm, fetch=True)
        return response
    
    @staticmethod
    def get_fields_starting_with(name):
        comm = f'''select * from field
        where field_name like '{name}%';'''
        response = db.run(comm, fetch=True)
        return response
    
    @staticmethod
    def get_fields_sorted_by_rating_asc():
        comm = f'''select * from field
        order by rating asc;'''
        response = db.run(comm, fetch=True)
        return response
    
    @staticmethod
    def get_fields_sorted_by_rating_desc():
        comm = f'''select * from field
        order by rating desc;'''
        response = db.run(comm, fetch=True)
        return response
    
    @staticmethod
    def get_field(field_id):
        comm = f'''select * from field
        where field_id={field_id};'''
        response = db.run(comm, fetch=True)
        return response
    
    @staticmethod
    def get_field_reviews(field_id):
        response = Field.get_field(field_id)
        if isinstance(response, list):
            field_id = response[0][0]
            comm = f'''select * from review
            where field_id = '{field_id}';'''
            response = db.run(comm, fetch=True)
        return response