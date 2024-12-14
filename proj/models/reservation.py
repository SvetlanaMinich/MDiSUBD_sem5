from db_service import DataBaseService

db = DataBaseService()

class Reservation:
    @staticmethod
    def create_reservation(client_id,
                           schedule_id):
        comm = f'''insert into reservation
        (client_id, schedule_id)
        values
        ({client_id}, {schedule_id});'''
        response = db.run(comm, fetch=False)
        return response
    
    @staticmethod
    def delete_reservation(reservation_id):
        comm = f'''call delete_reservation({reservation_id});'''
        response = db.run(comm, fetch=False)
        return response
    
    @staticmethod
    def get_all_reservations():
        comm = f'''select * from reservation;'''
        response = db.run(comm, fetch=True)
        return response
    
    @staticmethod
    def get_reservations_by_client(client_id):
        comm = f'''select * from reservation
        where client_id={client_id};'''
        response = db.run(comm, fetch=True)
        return response
    
    @staticmethod
    def get_reservation(reservation_id):
        comm = f'''select * from reservation
        where reservation_id={reservation_id};'''
        response = db.run(comm, fetch=True)
        return response
    

    @staticmethod
    def get_field_by_reservation(reservation_id):
        comm = f'''call get_field_by_reservation({reservation_id}, null);'''
        response = db.run(comm, fetch=True)
        if isinstance(response, list):
            f_id = response[0][0]
            comm = f'''select * from field
            where field_id={f_id}'''
            response = db.run(comm, fetch=True)
        return response