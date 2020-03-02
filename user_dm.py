from psycopg2 import sql
import db, os, bcrypt


def random_api_key():
    return os.urandom(100)


# hash plain text pass
def hash_password(text_password):
    hashed_pass = bcrypt.hashpw(text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_pass.decode('utf-8')


# verify plain text pass with encrypted db pass
def verify_password(text_password, hashed_pass):
    return bcrypt.checkpw(text_password.encode('utf-8'), hashed_pass.encode('utf-8'))


@db.use
def add_user(cursor, username, password):
    cursor.execute(
        sql.SQL("""
            INSERT INTO users ({col1}, {col2})
            VALUES (%s, %s);
        """).format(
            col1=sql.Identifier('username'),
            col2=sql.Identifier('password')
        ), [username, password]
    )


@db.use
def check_user(cursor, username):
    query = """
        SELECT id, password
        FROM users
        WHERE username ILIKE %(username)s;
    """
    data = {
        "username": username
    }
    cursor.execute(query, data)
    return cursor.fetchone()
