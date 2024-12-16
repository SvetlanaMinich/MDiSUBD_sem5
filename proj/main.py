from typing import Annotated
from models.field import Field
from models.review import Review
from models.schedule import Schedule
from models.client import Client
from models.admin import Admin
from models.reservation import Reservation
from models.models import *

import logging

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fastui.forms import fastui_form
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayLookup, DisplayMode
from fastui.events import GoToEvent, BackEvent

logger = logging.getLogger(name='APP')

current_client_id = None
current_admin_id = None

app = FastAPI()
# uvicorn main:app --host 0.0.0.0 --port 80

@app.get('/api/', response_model=FastUI, response_model_exclude_none=True)
def start_page() -> list[AnyComponent]:
    '''Главная страница'''
    return [
            c.Page(
                components=[
                    c.Button(text='Список полей', on_click=GoToEvent(url='/fields')),
                    c.Button(text='Расписание', on_click=GoToEvent(url='/schedule')),
                    c.Button(text='Регистрация', on_click=GoToEvent(url='/register')) if (not current_client_id and not current_admin_id)
                        else c.Button(text='Выйти', on_click=GoToEvent(url=f'/logout')),
                    c.Heading(text='Главная', level=1),
                ]
            ),
        ]


@app.post('/api/fields/set-price')
def set_sorted_price(form: Annotated[PriceFilterModel, fastui_form(PriceFilterModel)]):
    price = form.model_dump()
    return [c.FireEvent(event=GoToEvent(url=f'/fields?price_from={ price['price_from'] }&price_to={ price['price_to'] }'))]


@app.post('/api/fields/search')
def set_sorted_price(form: Annotated[FieldNameSearchModel, fastui_form(FieldNameSearchModel)]):
    name = form.model_dump()
    return [c.FireEvent(event=GoToEvent(url=f'/fields', query={'search_name':name['name']}))]


@app.post('/api/register-user')
def registrate_user(form: Annotated[ClientRegistrationModel, fastui_form(ClientRegistrationModel)]):
    global current_client_id
    client = form.model_dump()
    response = Client.create_client(name=client['client_name'],
                                    surname=client['client_surname'],
                                    birth_date=client['birth_date'],
                                    login=client['client_login'],
                                    password=client['client_password'])
    if response==200:
        client_id = Client.get_client(login=client['client_login'],
                                      password=client['client_password'])
        current_client_id = client_id[0][0]
        return [c.FireEvent(event=GoToEvent(url=f'/user/{client_id[0][0]}'))]

    logger.error(response)
    return [c.FireEvent(event=GoToEvent(url=f'/register'))]


@app.post('/api/auth-user')
def auth_user(form: Annotated[ClientAuthModel, fastui_form(ClientAuthModel)]):
    global current_client_id, current_admin_id
    client = form.model_dump()
    response = Client.get_client(login=client['client_login'],
                                  password=client['client_password'])
    if isinstance(response, list):
        current_client_id = response[0][0]
        return [c.FireEvent(event=GoToEvent(url=f'/user/{response[0][0]}'))]
    
    else:
        response = Admin.get_admin(login=client['client_login'],
                                   password=client['client_password'])
        if isinstance(response, list):
            current_admin_id = response[0][0]
            return [c.FireEvent(event=GoToEvent(url=f'/admin/{response[0][0]}'))]
    
    logger.error(response)
    return [c.FireEvent(event=GoToEvent(url=f'/login'))]


@app.get('/api/fields', response_model=FastUI, response_model_exclude_none=True)
def fields_page(price_from=0, price_to=200, search_name='') -> list[AnyComponent]:
    print(price_from)
    if search_name:
        response = Field.get_fields_with(name=search_name)
    elif float(price_from) > 0 or float(price_to) != 200:
        response = Field.get_fields_by_price(price_from=float(price_from),
                                             price_to=float(price_to))
    else:
        response = Field.get_all_fields()
        
    if isinstance(response, list):
        fields = [
            FieldModel(field_id=field[0],
                        field_name=field[1],
                        field_location=field[2],
                        price_per_hour=field[3],
                        rating=field[4])
            for field in response
        ]
        return [
            c.Page(
                components=[
                    c.Button(text='Список полей', on_click=GoToEvent(url='/fields')),
                    c.Button(text='Расписание', on_click=GoToEvent(url='/schedule')),
                    c.Button(text='Регистрация', on_click=GoToEvent(url='/register')) if (not current_client_id and not current_admin_id)
                        else c.Button(text='Выйти', on_click=GoToEvent(url=f'/logout')),

                    c.Heading(text='Список полей', level=1),
                    
                    c.ModelForm(
                        model=PriceFilterModel,
                        submit_url='/api/fields/set-price'
                    ),

                    c.ModelForm(
                        model=FieldNameSearchModel,
                        submit_url='/api/fields/search'
                    ),

                    c.Table(
                        data=fields,
                        data_model=FieldModel,
                        columns=[
                            DisplayLookup(field='field_name', title='Название', on_click=GoToEvent(url='/fields/{field_id}')),
                            DisplayLookup(field='field_location', title='Локация'),
                            DisplayLookup(field='price_per_hour', title='Стоимость за час'),
                            DisplayLookup(field='rating', title='Рейтинг'),
                        ],
                    ),
                ]
            ),
        ] 


@app.get('/api/fields/{field_id}', response_model=FastUI, response_model_exclude_none=True)
def get_field_by_id(field_id: int) -> list[AnyComponent]:
    global current_client_id
    response_field = Field.get_field(field_id)

    if isinstance(response_field, list):
        field_full = response_field[0]
        field = FieldModel(field_id=field_full[0],
                            field_name=field_full[1], 
                            field_location=field_full[2], 
                            price_per_hour=field_full[3],
                            rating=field_full[4])
        
        reviews = []
        schedules = []

        response_reviews = Review.get_reviews_by_field(field_id=field.field_id)
        if isinstance(response_reviews, list) and len(response_reviews)>0:
            reviews = [
                ReviewModel(
                    review_id=r[0],
                    client_id=r[1],
                    field_id=r[2],
                    text=r[3],
                    created_at=r[4], 
                    rating=r[5],                   
                )
                for r in response_reviews
            ]
        
        response_schedule = Schedule.get_schedules_by_field(field_id=field.field_id)
        if isinstance(response_schedule, list) and len(response_schedule)>0:
            
            schedules = [
                ScheduleModel(
                    schedule_id=s[0],
                    field_id=s[1],
                    time_from=s[2],
                    time_to=s[3],
                    is_available=s[4],
                )
                for s in response_schedule
            ]

        return [c.Page(
            components=[
                c.Button(text='Список полей', on_click=GoToEvent(url='/fields')),
                c.Button(text='Расписание', on_click=GoToEvent(url='/schedule')),
                c.Button(text='Регистрация', on_click=GoToEvent(url='/register')) if (not current_client_id and not current_admin_id)
                        else c.Button(text='Выйти', on_click=GoToEvent(url=f'/logout')),

                c.Link(components=[c.Heading(text='Назад', level=4)], on_click=BackEvent()),

                c.Heading(text=field.field_name, level=2),
                c.Details(data=field),
                c.Heading(text='Отзывы', level=2),
                c.Table(
                        data=reviews,
                        columns=[
                            DisplayLookup(field='client_id', title='ID клиента'),
                            DisplayLookup(field='rating', title='Рейтинг'),
                            DisplayLookup(field='text', title='Отзыв'),
                            DisplayLookup(field='created_at', title='Дата создания', mode=DisplayMode.date),
                        ],
                    ) if len(reviews) > 0 else c.Text(text='Отзывов нет'),
                c.Heading(text='Расписание', level=2),
                c.Table(
                        data=schedules,
                        data_model=ScheduleModel,
                        columns=[
                            DisplayLookup(field='time_from', title='Время начала', mode=DisplayMode.date),
                            DisplayLookup(field='time_to', title='Время окончания', mode=DisplayMode.date),
                            DisplayLookup(field='is_available', title='Доступно'),
                        ],
                    ) if len(schedules) > 0 else c.Text(text='Для данного поля доступного свободного времени нет'),
                
                c.Heading(text='Хотите забронировать поле?'),
                c.Button(text='Забронировать поле', on_click=GoToEvent(url=f'/user/make-reservation-page/{field_id}')) if current_client_id
                    else c.Text(text='Зарегистрируйтесь, чтобы забронировать поле')
            ]
        ),]
    return response_field


@app.get('/api/schedule', response_model=FastUI, response_model_exclude_none=True)
def schedule_page() -> list[AnyComponent]:
    """
    Страница с расписанием.
    """
    global current_client_id
    response = Schedule.get_all_schedules()
    if isinstance(response, list):
        schedules = [
            ScheduleModel(schedule_id=s[0],
                          field_id=s[1],
                          time_from=s[2],
                          time_to=s[3],
                          is_available=s[4])
            for s in response
        ]
        return [
            c.Page(
                components=[
                    c.Button(text='Список полей', on_click=GoToEvent(url='/fields')),
                    c.Button(text='Расписание', on_click=GoToEvent(url='/schedule')),
                    c.Button(text='Регистрация', on_click=GoToEvent(url='/register')) if (not current_client_id and not current_admin_id)
                        else c.Button(text='Выйти', on_click=GoToEvent(url=f'/logout')),

                    c.Heading(text='Расписание', level=1),

                    c.Table(
                        data=schedules,
                        data_model=ScheduleModel,
                        columns=[
                            DisplayLookup(field='schedule_id', title='ID'),
                            DisplayLookup(field='field_id', title='ID поля', on_click=GoToEvent(url='/fields/{field_id}')),
                            DisplayLookup(field='time_from', title='Время начала', mode=DisplayMode.date),
                            DisplayLookup(field='time_to', title='Время окончания', mode=DisplayMode.date),
                            DisplayLookup(field='is_available', title='Доступно'),
                        ],
                    ),

                    c.Heading(text='Хотите забронировать поле?'),
                    c.ModelForm(
                        model=SelectScheduleForReservationModel,
                        submit_url=f'/api/user/select-schedule-for-reservation'
                    ) if current_client_id else c.Text(text='Зарегистрируйтесь, чтобы забронировать поле') 
                ]
            ),
        ]

@app.get('/api/register', response_model=FastUI, response_model_exclude_none=True)
def register_page() -> list[AnyComponent]:
    """
    Страница регистрации.
    """
    return [
        c.Page(
            components=[
                c.Button(text='Список полей', on_click=GoToEvent(url='/fields')),
                c.Button(text='Расписание', on_click=GoToEvent(url='/schedule')),
                c.Button(text='Регистрация', on_click=GoToEvent(url='/register')),

                c.Heading(text='Регистрация', level=1),

                c.ModelForm(
                        model=ClientRegistrationModel,
                        submit_url='/api/register-user'
                    ),
                
                c.Button(text='Уже есть аккаунт', on_click=GoToEvent(url='/login'))
            ]
        ),
    ]

@app.get('/api/login', response_model=FastUI, response_model_exclude_none=True)
def login_page() -> list[AnyComponent]:
    """
    Страница входа.
    """
    return [
        c.Page(
            components=[
                c.Button(text='Список полей', on_click=GoToEvent(url='/fields')),
                c.Button(text='Расписание', on_click=GoToEvent(url='/schedule')),
                c.Button(text='Регистрация', on_click=GoToEvent(url='/register')),

                c.Heading(text='Вход', level=1),

                c.ModelForm(
                        model=ClientAuthModel,
                        submit_url='/api/auth-user'
                    ),
                
                c.Button(text='Еще нет аккаунта', on_click=GoToEvent(url='/register'))
            ]
        ),
    ]


@app.get('/api/logout', response_model=FastUI, response_model_exclude_none=True)
def logout():
    global current_admin_id, current_client_id
    current_client_id = None 
    current_admin_id = None
    return [c.FireEvent(event=GoToEvent(url=f'/'))]



# ===========================
# ADMIN
# ===========================

# --------------------------- admin field --------------------------------

@app.post('/api/admin/remove-field')
def admin_remove_field(form: Annotated[DeleteFieldModel, fastui_form(DeleteFieldModel)]):
    field_id = form.model_dump()['field_id']
    print(field_id)
    response = Field.delete_field(field_id=field_id)
    if response!=200:
        logger.error(response)
    return [c.FireEvent(event=GoToEvent(url=f'/admin/fields-ad'))]

@app.post('/api/admin/add-field')
def admin_add_field(form: Annotated[AddFieldModel, fastui_form(AddFieldModel)]):
    field = form.model_dump()
    response = Field.create_field(name=field['field_name'],
                                  location=field['field_location'],
                                  price_per_hour=field['price_per_hour'])
    print(response)
    if response!=200:
        logger.error(response)
    return [c.FireEvent(event=GoToEvent(url=f'/admin/fields-ad'))]

@app.get('/api/admin/add-field-page', response_model=FastUI, response_model_exclude_none=True)
def add_field() -> list[AnyComponent]:
    return [
        c.Page(
            components=[
                c.Button(text='Список полей', on_click=GoToEvent(url='/admin/fields-ad')),
                c.Text(text='   '),
                c.Button(text='Отзывы', on_click=GoToEvent(url='/admin/reviews-ad')),
                c.Text(text='   '),
                c.Button(text='Расписание ', on_click=GoToEvent(url='/admin/schedule-ad')),
                c.Text(text='   '),
                c.Button(text='Выйти ', on_click=GoToEvent(url=f'/logout')),

                c.Heading(text='Новое поле', level=1),

                c.ModelForm(
                        model=AddFieldModel,
                        submit_url='/api/admin/add-field'
                    ),
                
                c.Link(components=[c.Heading(text='Назад', level=4)], on_click=BackEvent()),
            ]
        ),
    ]

@app.post('/api/admin/update-field/{field_id}')
def admin_update_field(field_id:int, form: Annotated[AddFieldModel, fastui_form(AddFieldModel)]):
    field = form.model_dump()
    Field.update_field_name(field_id=field_id, new_name=field['field_name'])
    Field.update_field_location(field_id=field_id, new_location=field['field_location'])
    Field.update_field_price(field_id=field_id, new_price=field['price_per_hour'])
    return [c.FireEvent(event=GoToEvent(url=f'/admin/fields-ad/{field_id}'))]

@app.get('/api/admin/update-field-page/{field_id}', response_model=FastUI, response_model_exclude_none=True)
def update_field(field_id: int) -> list[AnyComponent]:
    response = Field.get_field(field_id=field_id)
    if isinstance(response, list):
        field = AddFieldModel(
            field_name=response[0][1],
            field_location=response[0][2],
            price_per_hour=response[0][3],
        )
    return [
        c.Page(
            components=[
                c.Button(text='Список полей', on_click=GoToEvent(url='/admin/fields-ad')),
                c.Text(text='   '),
                c.Button(text='Отзывы', on_click=GoToEvent(url='/admin/reviews-ad')),
                c.Text(text='   '),
                c.Button(text='Расписание ', on_click=GoToEvent(url='/admin/schedule-ad')),
                c.Text(text='   '),
                c.Button(text='Выйти ', on_click=GoToEvent(url=f'/logout')),

                c.Heading(text='Изменить поле ' + field.field_name, level=1),

                c.ModelForm(
                        model=AddFieldModel,
                        submit_url=f'/api/admin/update-field/{response[0][0]}'
                    ),
                
                c.Link(components=[c.Heading(text='Назад', level=4)], on_click=BackEvent()),
            ]
        ),
    ]


@app.get('/api/admin/fields-ad', response_model=FastUI, response_model_exclude_none=True)
def admin_fields_page() -> list[AnyComponent]:
    response = Field.get_all_fields()
    if isinstance(response, list):
        fields = [
            FieldModel(field_id=field[0],
                        field_name=field[1],
                        field_location=field[2],
                        price_per_hour=field[3],
                        rating=field[4])
            for field in response
        ]
        return [
            c.Page(
                components=[
                    c.Button(text='Список полей', on_click=GoToEvent(url='/admin/fields-ad')),
                    c.Text(text='   '),
                    c.Button(text='Отзывы', on_click=GoToEvent(url='/admin/reviews-ad')),
                    c.Text(text='   '),
                    c.Button(text='Расписание ', on_click=GoToEvent(url='/admin/schedule-ad')),
                    c.Text(text='   '),
                    c.Button(text='Выйти ', on_click=GoToEvent(url=f'/logout')),

                    c.Heading(text='Список полей', level=1),

                    c.Heading(text='Удалить', level=4),
                    c.ModelForm(
                        model=DeleteFieldModel,
                        submit_url='/api/admin/remove-field'
                    ),

                    c.Button(text='Добавить поле', on_click=GoToEvent(url='/admin/add-field-page')),
                    
                    c.Table(
                        data=fields,
                        data_model=FieldModel,
                        columns=[
                            DisplayLookup(field='field_id', title='ID'),
                            DisplayLookup(field='field_name', title='Название', on_click=GoToEvent(url='/admin/fields-ad/{field_id}')),
                            DisplayLookup(field='field_location', title='Локация'),
                            DisplayLookup(field='price_per_hour', title='Стоимость за час'),
                            DisplayLookup(field='rating', title='Рейтинг'),
                        ],
                    ),
                ]
            ),
        ] 


@app.get('/api/admin/fields-ad/{field_id}', response_model=FastUI, response_model_exclude_none=True)
def admin_field_by_id(field_id: int) -> list[AnyComponent]:
    response_field = Field.get_field(field_id)

    if isinstance(response_field, list):
        field_full = response_field[0]
        field = FieldModel(field_id=field_full[0],
                            field_name=field_full[1], 
                            field_location=field_full[2], 
                            price_per_hour=field_full[3],
                            rating=field_full[4])
        
        reviews = []
        schedules = []

        response_reviews = Review.get_reviews_by_field(field_id=field.field_id)
        if isinstance(response_reviews, list) and len(response_reviews)>0:
            reviews = [
                ReviewModel(
                    review_id=r[0],
                    client_id=r[1],
                    field_id=r[2],
                    text=r[3],
                    created_at=r[4], 
                    rating=r[5],                   
                )
                for r in response_reviews
            ]
        
        response_schedule = Schedule.get_schedules_by_field(field_id=field.field_id)
        if isinstance(response_schedule, list) and len(response_schedule)>0:
            
            schedules = [
                ScheduleModel(
                    schedule_id=s[0],
                    field_id=s[1],
                    time_from=s[2],
                    time_to=s[3],
                    is_available=s[4],
                )
                for s in response_schedule
            ]

        return [c.Page(
            components=[
                c.Button(text='Список полей', on_click=GoToEvent(url='/admin/fields-ad')),
                c.Text(text='   '),
                c.Button(text='Отзывы', on_click=GoToEvent(url='/admin/reviews-ad')),
                c.Text(text='   '),
                c.Button(text='Расписание ', on_click=GoToEvent(url='/admin/schedule-ad')),
                c.Text(text='   '),
                c.Button(text='Выйти ', on_click=GoToEvent(url=f'/logout')),

                c.Link(components=[c.Heading(text='Назад', level=4)], on_click=BackEvent()),

                c.Heading(text=field.field_name, level=2),
                c.Details(data=field),
                c.Button(text='Изменить поле', on_click=GoToEvent(url=f'/admin/update-field-page/{field.field_id}')),
                c.Heading(text='Отзывы', level=2),
                c.Table(
                        data=reviews,
                        columns=[
                            DisplayLookup(field='client_id', title='ID клиента'),
                            DisplayLookup(field='rating', title='Рейтинг'),
                            DisplayLookup(field='text', title='Отзыв'),
                            DisplayLookup(field='created_at', title='Дата создания', mode=DisplayMode.date),
                        ],
                    ) if len(reviews) > 0 else c.Text(text='Отзывов нет'),
                c.Heading(text='Расписание', level=2),
                c.Table(
                        data=schedules,
                        columns=[
                            DisplayLookup(field='time_from', title='Время начала', mode=DisplayMode.date),
                            DisplayLookup(field='time_to', title='Время окончания', mode=DisplayMode.date),
                            DisplayLookup(field='is_available', title='Доступно'),
                        ],
                    ) if len(schedules) > 0 else c.Text(text='Для данного поля доступного свободного времени нет'),
            ]
        ),]
    return response_field

#---------------------- admin schedule -------------------------

@app.post('/api/admin/delete-schedule')
def admin_delete_schedule(form: Annotated[DeleteScheduleModel, fastui_form(DeleteScheduleModel)]):
    schedule_id = form.model_dump()['schedule_id']
    response = Schedule.delete_schedule(schedule_id=schedule_id)
    if response!=200:
        logger.error(response)
    return [c.FireEvent(event=GoToEvent(url=f'/admin/schedule-ad'))]

@app.post('/api/admin/add-schedule')
def admin_add_schedule(form: Annotated[AddScheduleModel, fastui_form(AddScheduleModel)]):
    schedule = form.model_dump()
    
    response = Schedule.create_schedule(field_id=schedule['field_id'],
                                        time_from=schedule['time_from'],
                                        time_to=schedule['time_to'])
    if response!=200:
        logger.error(response)
    return [c.FireEvent(event=GoToEvent(url=f'/admin/schedule-ad'))]

@app.get('/api/admin/add-schedule-page', response_model=FastUI, response_model_exclude_none=True)
def add_schedule_page() -> list[AnyComponent]:
    fields = []
    response = Field.get_all_fields()
    if isinstance(response, list):
        fields = [
            FieldModel(field_id=field[0],
                        field_name=field[1],
                        field_location=field[2],
                        price_per_hour=field[3],
                        rating=field[4])
            for field in response
        ]

    return [
        c.Page(
            components=[
                c.Button(text='Список полей', on_click=GoToEvent(url='/admin/fields-ad')),
                c.Text(text='   '),
                c.Button(text='Отзывы', on_click=GoToEvent(url='/admin/reviews-ad')),
                c.Text(text='   '),
                c.Button(text='Расписание ', on_click=GoToEvent(url='/admin/schedule-ad')),
                c.Text(text='   '),
                c.Button(text='Выйти ', on_click=GoToEvent(url=f'/logout')),

                c.Heading(text='Новый элемент расписания', level=1),

                c.Text(text='Доступные поля'),
                c.Table(
                        data=fields,
                        data_model=FieldModel,
                        columns=[
                            DisplayLookup(field='field_id', title='ID'),
                            DisplayLookup(field='field_name', title='Название', on_click=GoToEvent(url='/admin/fields-ad/{field_id}')),
                            DisplayLookup(field='field_location', title='Локация'),
                            DisplayLookup(field='price_per_hour', title='Стоимость за час'),
                            DisplayLookup(field='rating', title='Рейтинг'),
                        ],
                    ),

                c.ModelForm(
                        model=AddScheduleModel,
                        submit_url='/api/admin/add-schedule'
                    ),
                
                c.Link(components=[c.Heading(text='Назад', level=4)], on_click=BackEvent()),
            ]
        ),
    ]

@app.get('/api/admin/schedule-ad', response_model=FastUI, response_model_exclude_none=True)
def admin_schedule_page() -> list[AnyComponent]:
    """
    Страница с расписанием.
    """
    response = Schedule.get_all_schedules()
    if isinstance(response, list):
        schedules = [
            ScheduleModel(schedule_id=s[0],
                          field_id=s[1],
                          time_from=s[2],
                          time_to=s[3],
                          is_available=s[4])
            for s in response
        ]
        return [
            c.Page(
                components=[
                    c.Button(text='Список полей', on_click=GoToEvent(url='/admin/fields-ad')),
                    c.Text(text='   '),
                    c.Button(text='Отзывы', on_click=GoToEvent(url='/admin/reviews-ad')),
                    c.Text(text='   '),
                    c.Button(text='Расписание ', on_click=GoToEvent(url='/admin/schedule-ad')),
                    c.Text(text='   '),
                    c.Button(text='Выйти ', on_click=GoToEvent(url=f'/logout')),

                    c.Heading(text='Расписание', level=1),

                    c.Heading(text='Удалить', level=4),
                    c.ModelForm(
                        model=DeleteScheduleModel,
                        submit_url='/api/admin/delete-schedule'
                    ),

                    c.Button(text='Добавить расписание', on_click=GoToEvent(url='/admin/add-schedule-page')),

                    c.Table(
                        data=schedules,
                        data_model=ScheduleModel,
                        columns=[
                            DisplayLookup(field='schedule_id', title='ID'),
                            DisplayLookup(field='field_id', title='ID поля', on_click=GoToEvent(url='/admin/fields-ad/{field_id}')),
                            DisplayLookup(field='time_from', title='Время начала', mode=DisplayMode.date),
                            DisplayLookup(field='time_to', title='Время окончания', mode=DisplayMode.date),
                            DisplayLookup(field='is_available', title='Доступно'),
                        ],
                    ),
                ]
            ),
        ]


# ----------------------------- admin reviews --------------------------------

@app.post('/api/admin/delete-review')
def admin_delete_review(form: Annotated[DeleteReviewModel, fastui_form(DeleteReviewModel)]):
    review_id = form.model_dump()['review_id']
    response = Review.delete_review(review_id=review_id)
    if response!=200:
        logger.error(response)
    return [c.FireEvent(event=GoToEvent(url=f'/admin/reviews-ad'))]


@app.get('/api/admin/reviews-ad', response_model=FastUI, response_model_exclude_none=True)
def admin_reviews_page() -> list[AnyComponent]:
    """
    Страница с отзывами.
    """
    response = Review.get_all_reviews()
    if isinstance(response, list):
        reviews = [
            ReviewModel(
                    review_id=r[0],
                    client_id=r[1],
                    field_id=r[2],
                    text=r[3],
                    created_at=r[4], 
                    rating=r[5],                   
                )
            for r in response
        ]
        return [
            c.Page(
                components=[
                    c.Button(text='Список полей', on_click=GoToEvent(url='/admin/fields-ad')),
                    c.Text(text='   '),
                    c.Button(text='Отзывы', on_click=GoToEvent(url='/admin/reviews-ad')),
                    c.Text(text='   '),
                    c.Button(text='Расписание ', on_click=GoToEvent(url='/admin/schedule-ad')),
                    c.Text(text='   '),
                    c.Button(text='Выйти ', on_click=GoToEvent(url=f'/logout')),

                    c.Heading(text='Расписание', level=1),

                    c.Heading(text='Удалить', level=4),
                    c.ModelForm(
                        model=DeleteReviewModel,
                        submit_url='/api/admin/delete-review'
                    ),

                    c.Table(
                        data=reviews,
                        data_model=ReviewModel,
                        columns=[
                            DisplayLookup(field='review_id', title='ID'),
                            DisplayLookup(field='client_id', title='ID клиента'),
                            DisplayLookup(field='rating', title='Рейтинг'),
                            DisplayLookup(field='text', title='Отзыв'),
                            DisplayLookup(field='created_at', title='Дата создания', mode=DisplayMode.date),
                        ],
                    ),
                ]
            ),
        ]


@app.get('/api/admin/{client_id}', response_model=FastUI, response_model_exclude_none=True)
def admin_page(client_id:int) -> list[AnyComponent]:
    """
    Страница админа.
    """
    global current_admin_id
    current_admin_id = client_id
    response = Admin.get_admin_by_id(client_id)
    return [
        c.Page(
            components=[
                c.Button(text='Список полей', on_click=GoToEvent(url='/admin/fields-ad')),
                c.Text(text='   '),
                c.Button(text='Отзывы', on_click=GoToEvent(url='/admin/reviews-ad')),
                c.Text(text='   '),
                c.Button(text='Расписание ', on_click=GoToEvent(url='/admin/schedule-ad')),
                c.Text(text='   '),
                c.Button(text='Выйти ', on_click=GoToEvent(url=f'/logout')),

                c.Heading(text='Админ ' + response[0][1], level=1),
            ]
        ),
    ]


# ====================
# CLIENT
# ====================

# --------------------------------- USER PAGE

@app.get('/api/user/{client_id}', response_model=FastUI, response_model_exclude_none=True)
def user_page(client_id:int) -> list[AnyComponent]:
    """
    Страница пользователя.
    """
    global current_client_id
    current_client_id = client_id
    response = Client.get_client_by_id(client_id=client_id)
    client = ClientRegistrationModel(
        client_name=response[0][1],
        client_surname=response[0][2],
        birth_date=response[0][3],
        client_login='',
        client_password='',
    )
    response = Client.get_client_login(client_id=client_id)
    client.client_login = response[0][0]
    response = Client.get_client_password(client_id=client_id)
    client.client_password = response[0][0]

    response = Reservation.get_reservations_by_client(client_id=client_id)
    reservations = []
    if isinstance(response, list):
        reservations = [
            ReservationModel(
                reservation_id=r[0],
                client_id=r[1],
                schedule_id=r[2],
                created_at=r[3]
            )
            for r in response
        ]
    schedules = []
    for r in reservations:
        response = Schedule.get_schedule(schedule_id=r.schedule_id)
        if isinstance(response, list):
            schedules.append(ScheduleModel(
                schedule_id=response[0][0],
                field_id=response[0][1],
                time_from=response[0][2],
                time_to=response[0][3],
                is_available=False
            ))

    return [
        c.Page(
            components=[
                c.Button(text='Список полей', on_click=GoToEvent(url='/fields')),
                c.Text(text='   '),
                c.Button(text='Расписание', on_click=GoToEvent(url='/schedule')),
                c.Text(text='   '),
                c.Button(text='Выйти', on_click=GoToEvent(url=f'/logout')),
                c.Text(text='                         '),
                
                c.Heading(text='Клиент   ' + client.client_name, level=1),
                c.Text(text=client.client_name.capitalize() + '  ' + client.client_surname.capitalize()),
                c.Heading(text='Birth date:   ' + str(client.birth_date), level=5),

                
                c.Button(text='Изменить информацию о себе', on_click=GoToEvent(url=f'/user/{client_id}/update-bio-page')),
                c.Text(text='    '),
                c.Button(text='Изменить логин или (и) пароль', on_click=GoToEvent(url=f'/user/{client_id}/update-creds-page')),
                c.Text(text='    '),
                c.Button(text='Добавить способ оплаты', on_click=GoToEvent(url=f'/user/{client_id}/add-payment-page')),
                c.Text(text='    '),
                c.Button(text='Удалить способ оплаты', on_click=GoToEvent(url=f'/user/{client_id}/delete-payment-page')),
                c.Heading(text='Мои брони:      '),
                c.Button(text='Забронировать поле', on_click=GoToEvent(url=f'/user/make-reservation-page/0')),

                c.Table(
                    data=reservations,
                    data_model=ReservationModel,
                    columns=[
                        DisplayLookup(field='reservation_id', title='ID'),
                        DisplayLookup(field='schedule_id', title='ID расписания'),
                        DisplayLookup(field='created_at', title='Время бронирования', mode=DisplayMode.datetime),
                    ],
                ),
                c.Heading(text='Расписания брони:      '),
                c.Table(
                    data=schedules,
                    data_model=ScheduleModel,
                    columns=[
                        DisplayLookup(field='schedule_id', title='ID'),
                        DisplayLookup(field='field_id', title='ID поля'),
                        DisplayLookup(field='time_from', title='Время начала', mode=DisplayMode.datetime),
                        DisplayLookup(field='time_to', title='Время окончания', mode=DisplayMode.datetime),
                    ],
                ),

                c.Heading(text='Удалить бронь', level=3),
                c.ModelForm(
                        model=DeleteReservationModel,
                        submit_url=f'/api/user/delete-reservation'
                    ),
            ]
        ),
    ]


@app.post('/api/user/{client_id}/update-bio')
def update_bio(client_id:int, form: Annotated[ClientBioModel, fastui_form(ClientBioModel)]):
    client = form.model_dump()
    response = Client.update_client_name(client_id=client_id,
                                         name=client['client_name'])
    response = Client.update_client_surname(client_id=client_id,
                                            surname=client['client_surname'])
    response = Client.update_client_birth_date(client_id=client_id,
                                               birth_date=client['birth_date'])
    if response!=200:
        logger.error(response)
    return [c.FireEvent(event=GoToEvent(url=f'/user/{client_id}'))]

@app.get('/api/user/{client_id}/update-bio-page', response_model=FastUI, response_model_exclude_none=True)
def update_bio_page(client_id:int) -> list[AnyComponent]:
    """
    Страница изменения данных о пользователе.
    """
    return [
        c.Page(
            components=[
                c.Button(text='Список полей', on_click=GoToEvent(url='/user/fields')),
                c.Text(text='   '),
                c.Button(text='Расписание', on_click=GoToEvent(url='/user/schedule')),
                c.Text(text='   '),
                c.Button(text='Выйти', on_click=GoToEvent(url=f'/logout')),
                c.Text(text='                         '),
                c.Link(components=[c.Heading(text='Назад', level=4)], on_click=BackEvent()),
                
                c.Heading(text='Изменить информацию о себе', level=3),
                c.ModelForm(
                        model=ClientBioModel,
                        submit_url=f'/api/user/{client_id}/update-bio'
                    ),
            ]
        ),
    ]


@app.post('/api/user/{client_id}/update-creds')
def update_creds(client_id:int, form: Annotated[ClientCredsModel, fastui_form(ClientCredsModel)]):
    client = form.model_dump()
    print(client)
    response = Client.update_client_credentials(client_id=client_id,
                                                login=client['client_login'],
                                                password=client['client_password'])
    if response!=200:
        logger.error(response)
    return [c.FireEvent(event=GoToEvent(url=f'/user/{client_id}'))]

@app.get('/api/user/{client_id}/update-creds-page', response_model=FastUI, response_model_exclude_none=True)
def update_creds_page(client_id:int) -> list[AnyComponent]:
    """
    Страница изменения личных данных о пользователе.
    """
    return [
        c.Page(
            components=[
                c.Button(text='Список полей', on_click=GoToEvent(url='/user/fields')),
                c.Text(text='   '),
                c.Button(text='Расписание', on_click=GoToEvent(url='/user/schedule')),
                c.Text(text='   '),
                c.Button(text='Выйти', on_click=GoToEvent(url=f'/logout')),
                c.Text(text='                         '),
                c.Link(components=[c.Heading(text='Назад', level=4)], on_click=BackEvent()),
                
                c.Heading(text='Изменить логин и (или) пароль', level=3),
                c.ModelForm(
                        model=ClientCredsModel,
                        submit_url=f'/api/user/{client_id}/update-creds'
                    ),
            ]
        ),
    ]


@app.post('/api/user/{client_id}/add-payment')
def update_payment(client_id:int, form: Annotated[ClientAddPaymentModel, fastui_form(ClientAddPaymentModel)]):
    client = form.model_dump()
    response = Client.create_client_payment(client_id=client_id,
                                            card_iban=client['card_iban'])
    if response!=200:
        logger.error(response)
    return [c.FireEvent(event=GoToEvent(url=f'/user/{client_id}'))]

@app.get('/api/user/{client_id}/add-payment-page', response_model=FastUI, response_model_exclude_none=True)
def update_payment_page(client_id:int) -> list[AnyComponent]:
    """
    Страница изменения данных о пользователе.
    """
    return [
        c.Page(
            components=[
                c.Button(text='Список полей', on_click=GoToEvent(url='/user/fields')),
                c.Text(text='   '),
                c.Button(text='Расписание', on_click=GoToEvent(url='/user/schedule')),
                c.Text(text='   '),
                c.Button(text='Выйти', on_click=GoToEvent(url=f'/logout')),
                c.Text(text='                         '),
                c.Link(components=[c.Heading(text='Назад', level=4)], on_click=BackEvent()),
                
                c.Heading(text='Добавить карту', level=3),
                c.ModelForm(
                        model=ClientAddPaymentModel,
                        submit_url=f'/api/user/{client_id}/add-payment'
                    ),
            ]
        ),
    ]


@app.post('/api/user/{client_id}/delete-payment')
def delete_payment(client_id:int, form: Annotated[ClientAddPaymentModel, fastui_form(ClientAddPaymentModel)]):
    client = form.model_dump()
    response = Client.create_client_payment(client_id=client_id,
                                            card_iban=client['card_iban'])
    if response!=200:
        logger.error(response)
    return [c.FireEvent(event=GoToEvent(url=f'/user/{client_id}'))]

@app.get('/api/user/{client_id}/delete-payment-page', response_model=FastUI, response_model_exclude_none=True)
def delete_payment_page(client_id:int) -> list[AnyComponent]:
    """
    Страница изменения данных о пользователе.
    """
    response = Client.get_client_payments(client_id=client_id)
    payments = [
        ClientPaymentCredentialsModel(
            clientPaymentCredentials_id=p[0],
            client_id=p[1],
            card_iban=p[2]
        )
        for p in response
    ]
    return [
        c.Page(
            components=[
                c.Button(text='Список полей', on_click=GoToEvent(url='/user/fields')),
                c.Text(text='   '),
                c.Button(text='Расписание', on_click=GoToEvent(url='/user/schedule')),
                c.Text(text='   '),
                c.Button(text='Выйти', on_click=GoToEvent(url=f'/logout')),
                c.Text(text='                         '),
                c.Link(components=[c.Heading(text='Назад', level=4)], on_click=BackEvent()),
                c.Heading(text='Доступные карты клиента', level=2),
                c.Table(
                        data=payments,
                        data_model=ClientPaymentCredentialsModel,
                        columns=[
                            DisplayLookup(field='clientPaymentCredentials_id', title='ID'),
                            DisplayLookup(field='card_iban', title='IBAN'),
                        ],
                    ),
                
                c.Heading(text='Удалить карту', level=3),
                c.ModelForm(
                        model=ClientAddPaymentModel,
                        submit_url=f'/api/user/{client_id}/delete-payment'
                    ),
            ]
        ),
    ]


# -------------------------- USER RESERVATION

@app.post('/api/user/delete-reservation')
def select_field(form: Annotated[DeleteReservationModel, fastui_form(DeleteReservationModel)]):
    global current_client_id
    reservation_id = form.model_dump()['reservation_id']
    response = Reservation.delete_reservation(reservation_id=reservation_id)
    if response!=200:
        logger.error(response)
    return [c.FireEvent(event=GoToEvent(url=f'/user/{current_client_id}'))]

@app.post('/api/user/select-field-for-reservation')
def select_field(form: Annotated[SelectFieldForReservationModel, fastui_form(SelectFieldForReservationModel)]):
    field_id = form.model_dump()['field_id']
    return [c.FireEvent(event=GoToEvent(url=f'/user/make-reservation-page/{field_id}'))]

@app.post('/api/user/select-schedule-for-reservation')
def select_field(form: Annotated[SelectScheduleForReservationModel, fastui_form(SelectScheduleForReservationModel)]):
    global current_client_id
    print(current_client_id)
    sch_id = form.model_dump()['schedule_id']
    response = Reservation.create_reservation(
        client_id=current_client_id,
        schedule_id=sch_id
    )
    if response!=200:
        logger.error(response)
    return [c.FireEvent(event=GoToEvent(url=f'/user/{current_client_id}'))]

@app.get('/api/user/make-reservation-page/{field_id}', response_model=FastUI, response_model_exclude_none=True)
def make_reservation_page(field_id: int) -> list[AnyComponent]:
    fields = []
    schedules = []
    if field_id == 0:
        response = Field.get_all_fields()
        fields = [
                FieldModel(field_id=field[0],
                            field_name=field[1],
                            field_location=field[2],
                            price_per_hour=field[3],
                            rating=field[4])
                for field in response
            ]
    else:
        response = Field.get_field(field_id=field_id)
        fields = [
                FieldModel(field_id=field[0],
                            field_name=field[1],
                            field_location=field[2],
                            price_per_hour=field[3],
                            rating=field[4])
                for field in response
            ]
        
        response = Schedule.get_schedules_by_field(field_id=field_id)
        schedules = [
            ScheduleModel(
                    schedule_id=s[0],
                    field_id=s[1],
                    time_from=s[2],
                    time_to=s[3],
                    is_available=s[4],
                )
            for s in response
        ]
    
    return c.Page(
        components=[
            c.Link(components=[c.Heading(text='Назад', level=4)], on_click=BackEvent()),
            c.Heading(text='Поля', level=2),
            c.Table(
                        data=fields,
                        data_model=FieldModel,
                        columns=[
                            DisplayLookup(field='field_id', title='ID'),
                            DisplayLookup(field='field_name', title='Название'),
                            DisplayLookup(field='field_location', title='Локация'),
                            DisplayLookup(field='price_per_hour', title='Стоимость за час'),
                            DisplayLookup(field='rating', title='Рейтинг'),
                        ],
                    ),
            c.ModelForm(
                model=SelectFieldForReservationModel,
                submit_url=f'/api/user/select-field-for-reservation'
            ) if field_id==0 else
            c.Table(
                        data=schedules,
                        data_model=ScheduleModel,
                        columns=[
                            DisplayLookup(field='schedule_id', title='ID'),
                            DisplayLookup(field='time_from', title='Время начала', mode=DisplayMode.datetime),
                            DisplayLookup(field='time_to', title='Время окончания', mode=DisplayMode.datetime),
                            DisplayLookup(field='is_available', title='Доступно'),
                        ],
                    ),
            c.ModelForm(
                    model=SelectScheduleForReservationModel,
                    submit_url=f'/api/user/select-schedule-for-reservation'
                ) if len(schedules) > 0 else c.Text(text='Доступного времени для бронирования нет'), 

        ]
    )



@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title='Proj'))
