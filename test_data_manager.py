import db

@db.use
def get_everything(cursor):
    query = f"""SELECT * FROM users;"""
    cursor.execute(query)
    return cursor.fetchall()