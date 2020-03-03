import db

@db.use
def get_everything(cursor):
    query = f"""SELECT * FROM urls;"""
    cursor.execute(query)
    return cursor.fetchall()