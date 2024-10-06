**Минич Светлана Владимировна, гр. 253503**
**Система бронирования спортивных площадок**
<hr>

**Функциональные требования к приложению:**
1. **Незарегистрированный пользователь**
- Просмотр информации о площадках
- Просмотр отзывов о площадках
- Просмотр расписания площадок
- Регистрация / (Авторизация/Аутентификация у зарегистрированного пользователя, но не в системе)
2. **Клиент (зарегистрированный пользователь)**
- Просмотр информации о площадках
- Просмотр отзывов о площадках
- Просмотр расписания площадок
- Бронирование площадки (CRUD)
- Просмотр истории бронирований
- Редактирование профиля
- Создание отзывов (CRUD)
3. **Администратор**
- Удаление пользователей, которые не заходили в аккаунт более 3 лет
- Управление площадками (CRUD)
- Управление расписанием (CRUD)
- Удаление нецензурных отзывов, спама
4. **Независящие от пользователя функции**
- Журналирование действий пользователя (вход в систему, регистрация, бронирование, редактирование профиля, отмена бронирования и т.д.)


**Сущности**
1. Field
*one-to-many with Review, Schedule, Reservation; Many-to-many with Client*
- id (INT, pk)
- field_name (VARCHAR, max_length=128)
- location (VARCHAR, max_length=128)
- price_per_hour (DECIMAL)
- rating (INT, max=5, min=1, default=None)
2. Review
*Many-to-one with Client, Field*
- id (INT, pk)
- client_id (INT, FK) 
- field_id (INT, FK)
- rating (INT, max=5, min=1, default=5)
- text (VARCHAR, max_length=512)
- created_at (DATETIME)
3. Schedule
*many-to-one with Field*
- id (INT, pk)
- field_id (INT, FK)
- time_from (DATETIME)
- time_to (DATETIME)
- available (BOOLEAN, default=TRUE)
4. Reservation
*Many-to-one wit Client, Field; One-to-one with Schedule*
- id (INT, pk)
- client_id (INT, FK)
- field_id (INT, FK)
- schedule_id (INT, FK)
- created_at (DATETIME)
5. Client
*One-to-many with Review, Reservation; One-to-one ClientCredentials, ClientPaymentCredentials; Many-to-many with Field, ClubCard*
- id (INT, pk)
- name (VARCHAR, max_length=32)
- surname (VARCHAR, max_length=32)
- birth_date (DATETIME)
6. ClientCredentials
*One-to-one with Client*
- id (INT, pk)
- client_id (INT, FK)
- login (VARCHAR, max_length=32, UNIQUE)
- password (VARCHAR, min_length=8, max_length=32)
7. ClientPaymentCredentials
*One-to-one with Client*
- id (INT, pk)  
- client_id (INT, FK)
- card_IBAN (VARCHAR, length=19)
- card_validity_period (DATETIME)
8. Admin
- id (INT, pk)
- nickname (VARCHAR, max_length=32)
- login (VARCHAR, max_length=32, UNIQUE)
- password (VARCHAR, min_length=8, max_length=32)
9. Logs 
*Many-to-one with Client*
- id (INT, pk)
- client_id (INT, FK)
- time (DATETIME)
- type (VARCHAR, max_length=32)
- text (TEXT)
10. ClubCard
*Many-to_many with Client, Many-to-One with Field*
- id (INT, pk)
- hours (INT)
- field_id (INT, FK)
11. ClientClubCard
*One-to-one with Client, ClubCard*
- id (INT, pk)
- client_id (INT, FK)
- clubcard_id (INT, FK)
- hours_left (INT, default=clubcard.hours)

