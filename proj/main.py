from db_service import DataBaseService
import datetime
from models.models import *
from models.field import Field
from models.schedule import Schedule
from models.clubcard import ClubCard
from models.client import Client
from models.reservation import Reservation

from fastapi import FastAPI, Query
from typing import List, Optional

app = FastAPI()


@app.get('/')
def start_page():
    return 'Welcome to my app!'


# -------------------------
# FIELD ENDPOINTS
# -------------------------
# @staticmethod
#     def get_fields_by_price(price_from=0, price_to=200):
#         comm = f'''select * from field
#         where price_per_hour >= {price_from} and price_per_hour <= {price_to};'''
#         response = db.run(comm, fetch=True)
#         return response
    
#     @staticmethod
#     def get_fields_starting_with(name):
#         comm = f'''select * from field
#         where field_name like '{name}%';'''
#         response = db.run(comm, fetch=True)
#         return response
    
#     @staticmethod
#     def get_fields_sorted_by_rating_asc():
#         comm = f'''select * from field
#         order by rating asc;'''
#         response = db.run(comm, fetch=True)
#         return response
    
#     @staticmethod
#     def get_fields_sorted_by_rating_desc():
#         comm = f'''select * from field
#         order by rating desc;'''
#         response = db.run(comm, fetch=True)
#         return response
    
#     @staticmethod
#     def get_field_reviews(field_id):
#         response = Field.get_field(field_id)
#         if isinstance(response, list):
#             field_id = response[0][0]
#             comm = f'''select * from review
#             where field_id = '{field_id}';'''
#             response = db.run(comm, fetch=True)
#         return response

@app.get('/fields')
def get_fields(field_id: Optional[int] = Query(None, description="ID of the field")):
    if not field_id:
        response = Field.get_all_fields()
        if isinstance(response, list):
            fields = [
                {
                    "field_id": field[0],
                    "field_name": field[1],
                    "field_location": field[2],
                    "price_per_hour": field[3],
                    "rating": field[4],
                }
                for field in response
            ]
            return fields
    else:
        response = Field.get_field(field_id)
        if isinstance(response, list):
            field_full = response[0]
            field = {
                "field_id": field_full[0],
                "field_name": field_full[1],
                "field_location": field_full[2],
                "price_per_hour": field_full[3],
                "rating": field_full[4],
            }
            return field
    return response


# -------------------------
# REVIEW ENDPOINTS
# -------------------------

# @app.get('/fields', response_model=List[FieldModel])
# def get_fields():
#     response = Field.get_all_fields()
#     if isinstance(response, list):
#         fields = [
#             {
#                 "field_id": field[0],
#                 "field_name": field[1],
#                 "field_location": field[2],
#                 "price_per_hour": field[3],
#                 "rating": field[4],
#             }
#             for field in response
#         ]
#         return fields
#     return response


# @app.get('/fields/{field_id}', response_model=FieldModel)
# def get_field_by_id(field_id: int):
#     response = Field.get_field(field_id)
#     if isinstance(response, list):
#         field_full = response[0]
#         field = {
#             "field_id": field_full[0],
#             "field_name": field_full[1],
#             "field_location": field_full[2],
#             "price_per_hour": field_full[3],
#             "rating": field_full[4],
#         }
#         return field
#     return response





if __name__ == '__main__':
    try:
        response = Reservation.get_field_by_reservation(2)
        
        if isinstance(response, list):  # Если ответ — это список данных
            for row in response:
                print(row)  # Печатаем каждую строк
        else:
            print(response)
    except Exception as ex:
        print(ex)

    # db.close_connection()