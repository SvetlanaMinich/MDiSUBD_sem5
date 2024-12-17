from pydantic import BaseModel
import datetime
import pydantic

class FieldModel(BaseModel):
    field_id: int
    field_name: str 
    field_location: str 
    price_per_hour: float 
    rating: int 

class AddFieldModel(BaseModel):
    field_name: str 
    field_location: str 
    price_per_hour: float


class FieldWithSchedulesModel(BaseModel):
    schedule_id: int
    field_name: str
    field_location: str
    price_per_hour: float
    rating: int
    time_from: datetime.datetime
    time_to: datetime.datetime


class ScheduleModel(BaseModel):
    schedule_id: int
    field_id: int
    time_from: datetime.datetime
    time_to: datetime.datetime
    is_available: bool

class DeleteScheduleModel(BaseModel):
    schedule_id: int

class AddScheduleModel(BaseModel):
    field_id: int
    time_from: datetime.datetime
    time_to: datetime.datetime



class ClientRegistrationModel(BaseModel):
    client_name: str
    client_surname: str
    birth_date: datetime.date
    client_login: str
    client_password: str


class ClientAuthModel(BaseModel):
    client_login: str
    client_password: str
  

class ClientPaymentCredentialsModel(BaseModel):
    clientPaymentCredentials_id: int
    client_id: int
    card_iban: str

class ClientBioModel(BaseModel):
    client_name: str
    client_surname: str
    birth_date: datetime.date

class ClientCredsModel(BaseModel):
    client_login: str
    client_password: str

class ClientAddPaymentModel(BaseModel):
    card_iban: str


class ReservationModel(BaseModel):
    reservation_id: int
    field_name: str
    time_from: datetime.datetime
    time_to: datetime.datetime

class SelectFieldForReservationModel(BaseModel):
    field_id: int

class SelectScheduleForReservationModel(BaseModel):
    schedule_id: int

class DeleteReservationModel(BaseModel):
    reservation_id: int


class ReviewModel(BaseModel):
    review_id: int
    client_id: int
    field_id: int
    rating: int
    text: str
    created_at: datetime.datetime

class DeleteReviewModel(BaseModel):
    review_id: int


class PriceFilterModel(BaseModel):
    price_from: float
    price_to: float

class FieldNameSearchModel(BaseModel):
    name: str

class DeleteFieldModel(BaseModel):
    field_id: str
