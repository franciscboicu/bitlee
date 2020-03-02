import psycopg2
import psycopg2.extras


def connect():
    try:
        connection = psycopg2.connect(
                user = 'francisc',
                password = '',
                host = 'localhost',
                database = 'shortify'
        )
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        raise exception
    return connection


def use(function):
    def wrapper(*args, **kwargs):
        connection = connect()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        data = function(cursor, *args, **kwargs)
        cursor.close()
        connection.close()
        return data
    return wrapper