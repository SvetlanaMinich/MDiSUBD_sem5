from db_service import DataBaseService
import datetime
from models.field import Field
from models.schedule import Schedule

if __name__ == '__main__':
    try:
        db = DataBaseService()
        comm = Schedule.get_schedules_by_field('field 1')
        response = db.run(command=comm, fetch=True)
        if isinstance(response, list):  # Если ответ — это список данных
            for row in response:
                print(row)  # Печатаем каждую строк
        else:
            print(response)
    except Exception as ex:
        print(ex)

    db.close_connection()