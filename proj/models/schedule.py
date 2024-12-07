class Schedule:
    @staticmethod
    def create_schedule(field_id, time_from, time_to, available=True):
        comm = f'''insert into schedule (field_id, time_from, time_to, is_available)
        values ({field_id}, '{time_from}', '{time_to}', {available});'''
        return comm

    @staticmethod
    def update_schedule_time(schedule_id, new_time_from, new_time_to):
        comm = f'''update schedule
        set time_from='{new_time_from}', time_to='{new_time_to}'
        where schedule_id={schedule_id};'''
        return comm

    @staticmethod
    def delete_schedule(schedule_id):
        comm = f'''delete from schedule
        where schedule_id={schedule_id};'''
        return comm

    @staticmethod
    def get_all_schedules():
        comm = f'''select * from schedule;'''
        return comm
    
    @staticmethod
    def get_schedules_by_field(field_name):
        comm = f'''call get_schedule_by_name('{field_name}', 0);'''
        return comm

    @staticmethod
    def get_schedules_by_date_from(date_from):
        comm = f'''select * from schedule
        where time_from >= '{date_from}';'''
        return comm
    
    @staticmethod
    def get_schedules_by_date_to(date_to):
        comm = f'''select * from schedule
        where time_to <= '{date_to}';'''
        return comm
    
    @staticmethod
    def get_schedules_sorted_by_time_asc():
        comm = f'''select * from schedule
        order by time_from asc;'''
        return comm