from config import *
import pymysql


class MainDataBase:

    def __init__(self):
        self.connection = pymysql.connect(
            host="localhost",
            user="root",
            password=PASSWORD,
            db=NAME,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )

    def add_contact(self, email, phone_number, package):
        try:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    _command = f'''INSERT INTO `contacts` (`email`, `phone_number`, `package`) VALUES (%s, %s, %s);'''
                    cursor.execute(_command, (email, phone_number, package))
                connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"add_contact_sql: {e}")
