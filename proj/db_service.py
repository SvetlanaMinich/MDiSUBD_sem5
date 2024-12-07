import creds
import psycopg2

class DataBaseService:
    def __init__(self):
        self.conn = psycopg2.connect(
            host = creds.hostname,
            dbname = creds.database,
            user = creds.username,
            password = creds.pwd,
            port = creds.port_id
        )

        self.curs = self.conn.cursor()

    
    def run(self, command, fetch=False):
        try:
            self.curs.execute(command)
            if fetch:  # Если нужно получить данные
                result = self.curs.fetchall()  # Получаем все строки результата
                return result
            self.conn.commit()
            return 200
        except Exception as ex:
            return ex


    def close_connection(self):
        self.curs.close()
        self.conn.close()