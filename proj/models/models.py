from pydantic import BaseModel
import datetime

class FieldModel(BaseModel):
    field_id: int
    field_name: str
    field_location: str
    price_per_hour: float
    rating: int


class ScheduleModel(BaseModel):
    schedule_id: int
    field_id: int
    time_from: datetime.datetime
    time_to: datetime.datetime
    is_available: bool


class ClientModel(BaseModel):
    client_id: int
    client_name: str
    client_surname: str
    birth_date: datetime.date


class ClientCredentialsModel(BaseModel):
    clientCredentials_id: int
    client_id: int
    client_login: str
    client_password: str


class ClientPaymentCredentialsModel(BaseModel):
    clientPaymentCredentials_id: int
    client_id: int
    card_iban: str


class AdminAccModel(BaseModel):
    adminAcc_id: int
    nickname: str
    login: str
    admin_password: str


class ReservationModel(BaseModel):
    reservation_id: int
    client_id: int
    schedule_id: int
    created_at: datetime.datetime


class ReviewModel(BaseModel):
    review_id: int
    client_id: int
    field_id: int
    rating: int
    text: str
    created_at: datetime.datetime