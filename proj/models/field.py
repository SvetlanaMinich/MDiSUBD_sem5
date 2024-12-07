class Field:
    @staticmethod
    def create_field(name,
                     location,
                     price_per_hour,
                     rating):
        comm = f'''insert into field (field_name, field_location, price_per_hour, rating)
        values ('{name}', '{location}', {price_per_hour}, {rating});'''
        return comm
    
    @staticmethod
    def update_field_name(old_name,
                          new_name):
        comm = f'''update field
        set field_name='{new_name}'
        where field_name='{old_name}';'''
        return comm
    
    @staticmethod
    def update_field_location(name,
                              new_location):
        comm = f'''update field
        set field_location='{new_location}'
        where field_name='{name}';'''
        return comm
    
    @staticmethod
    def update_field_price(name,
                           new_price):
        comm = f'''update field
        set price_per_hour={new_price}
        where field_name='{name}';'''
        return comm
    
    @staticmethod
    def delete_field(name):
        comm = f'''delete from field
        where field_name='{name}';'''
        return comm
    
    @staticmethod
    def get_all_fields():
        comm = f'''select * from field;'''
        return comm
    
    @staticmethod
    def get_fields_by_price(price_from=0, price_to=200):
        comm = f'''select * from field
        where price_per_hour >= {price_from} and price_per_hour <= {price_to};'''
        return comm
    
    @staticmethod
    def get_fields_starting_with(name):
        comm = f'''select * from field
        where field_name like '{name}%';'''
        return comm
    
    @staticmethod
    def get_fields_sorted_by_rating_asc():
        comm = f'''select * from field
        order by rating asc;'''
        return comm
    
    @staticmethod
    def get_fields_sorted_by_rating_desc():
        comm = f'''select * from field
        order by rating desc;'''
        return comm
    
    @staticmethod
    def get_field_by_name(name):
        comm = f'''select * from field
        where field_name = '{name}';'''
        return comm