import db, random,string

def generate_random_id(size=3):
    chars = string.ascii_uppercase
    chars += string.digits
    return ''.join(random.choice(chars) for _ in range(3))

@db.use
def get_url_by_shorten(cursor, code):
    query = """SELECT * FROM urls;"""
    cursor.execute(query)
    return cursor.fetchall()

@db.use
def check_if_short_url_exists(cursor,url):
    query = """SELECT * FROM urls WHERE url = %(url)s"""
    cursor.execute( query, {"url": url} )
    result = cursor.fetchone()

    if result:
        return True, result
    return False

@db.use
def update_views(cursor, id):
    query = """UPDATE urls SET views = views + 1 WHERE id = %(id)s"""
    cursor.execute( query, {"id": id} ) 


@db.use
def update_shortened(cursor, id):
    query = """UPDATE urls SET shortened = shortened + 1 WHERE id = %(id)s"""
    cursor.execute( query, {"id": id} )