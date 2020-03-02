import db


@db.use
def add_user(cursor, username, password):
    query = """
        INSERT INTO users
        (username, password)
        VALUES (%(username)s, %(password)s);
    """
    data = {
            "username": username,
            "password": password
            }
    cursor.execute(query, data)
add_user("alex", "123")