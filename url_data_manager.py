import db, random,string

def generate_random_id(size=3):
    chars = string.ascii_uppercase
    chars += string.digits
    return ''.join(random.choice(chars) for _ in range(size))

@db.use
def get_url_by_shorten(cursor, code):
    query = """SELECT * FROM urls;"""
    cursor.execute(query)
    return cursor.fetchall()

@db.use
def check_if_short_url_exists(cursor,short_url):
    query = """SELECT * FROM urls WHERE short_url = %(short_url)s"""
    cursor.execute( query, {"short_url": short_url} )
    result = cursor.fetchone()
    return result


@db.use
def check_if_url_exists(cursor,url):
    query = """SELECT * FROM urls WHERE url = %(url)s"""
    cursor.execute( query, {"url": url} )
    return cursor.fetchone()

@db.use
def update_views(cursor, id):
    query = """UPDATE urls SET views = views + 1 WHERE id = %(id)s"""
    cursor.execute( query, {"id": id} ) 


@db.use
def update_shortened(cursor, id):
    query = """UPDATE urls SET shortened = shortened + 1 WHERE id = %(id)s"""
    cursor.execute( query, {"id": id} )

@db.use
def add_url(cursor, data):
    query = """INSERT INTO urls (password,url,short_url,views,shortened) VALUES (%(password)s,%(url)s,%(short_url)s,%(views)s,%(shortened)s)"""
    cursor.execute( query, {
        'password': data['password'],
        'url': data['url'],
        'short_url': data['short_url'],
        'views': 0,
        'shortened': 1
    })