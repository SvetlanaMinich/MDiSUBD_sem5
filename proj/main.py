from db_service import DataBaseService
import datetime
from models.models import *
from models.field import Field
from models.schedule import Schedule
from models.clubcard import ClubCard
from models.client import Client
from models.reservation import Reservation
from models.review import Review

from fastapi import FastAPI, Query
from typing import List, Optional

app = FastAPI()


@app.get('/')
def start_page():
    return 'Welcome to my app!'


# -------------------------
# FIELD ENDPOINTS
# -------------------------

@app.get('/fields', response_model=List[FieldModel])
def get_fields():
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
    return response


@app.get('/fields/{field_id}', response_model=FieldModel)
def get_field_by_id(field_id: int):
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

@app.get('/reviews', response_model=List[ReviewModel])
def get_reviews():
    response = Review.get_all_reviews()
    if isinstance(response, list):
        reviews = [
            {
                "review_id": r[0],
                "client_id": r[1],
                "rating": r[2],                
                "text": r[3],
                "created_at": r[4],
                "field_id": r[5]
            }
            for r in response
        ]
        return reviews
    return response


@app.get('/reviews/{review_id}', response_model=ReviewModel)
def get_review_by_id(review_id: int):
    response = Review.get_review(review_id)
    if isinstance(response, list):
        r = response[0]
        review = {
                "review_id": r[0],
                "client_id": r[1],
                "rating": r[2],                
                "text": r[3],
                "created_at": r[4],
                "field_id": r[5]
            }
        return review
    return response





# if __name__ == '__main__':
#     try:
#         response = Reservation.get_field_by_reservation(2)
        
#         if isinstance(response, list):  # Если ответ — это список данных
#             for row in response:
#                 print(row)  # Печатаем каждую строк
#         else:
#             print(response)
#     except Exception as ex:
#         print(ex)

# db.close_connection()