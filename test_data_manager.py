import db, bcrypt


# hash plain text pass
def hash_password(text_password):
    return bcrypt.hashpw(text_password.encode('utf-8'), bcrypt.gensalt())


# verify plain text pass with encrypted db pass
def verify_password(text_password, hashed_pass):
    return bcrypt.checkpw(text_password.encode('utf-8'), hashed_pass.encode('utf-8'))


@db.use
def get_everything(cursor):
    query = f"""SELECT * FROM users;"""
    cursor.execute(query)
    return cursor.fetchall()


