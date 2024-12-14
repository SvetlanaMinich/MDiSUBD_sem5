from db_service import DataBaseService

db = DataBaseService()

class Review:
    @staticmethod
    def create_review(client_id,
                      text,
                      field_id,
                      rating=5):
        comm = f'''insert into review
        (client_id, rating, text, field_id)
        values
        ({client_id}, {rating}, '{text}', {field_id});'''
        response = db.run(comm, fetch=False)
        return response
    
    @staticmethod
    def update_review_text(review_id,
                           text):
        comm = f'''update review
        set text='{text}'
        where review_id={review_id};'''
        response = db.run(comm, fetch=False)
        return response
    
    @staticmethod
    def update_review_rating(review_id,
                             rating):
        comm = f'''update review
        set rating={rating}
        where review_id={review_id};'''
        response = db.run(comm, fetch=False)
        return response
    
    @staticmethod
    def delete_review(review_id):
        comm = f'''drop from review
        where review_id={review_id};'''
        response = db.run(comm, fetch=False)
        return response
    
    @staticmethod
    def get_review(review_id):
        comm = f'''select * from review
        where review_id={review_id};'''
        response = db.run(comm, fetch=True)
        return response
    
    @staticmethod
    def get_reviews_by_field(field_id):
        comm = f'''select * from review
        where field_id={field_id};'''
        response = db.run(comm, fetch=True)
        return response
    
    @staticmethod
    def get_all_reviews():
        comm = f'''select * from review;'''
        response = db.run(comm, fetch=True)
        return response