import db, random,string


def generate_random_id(size=3):
    chars = string.ascii_uppercase
    chars += string.digits
    return ''.join(random.choice(chars) for _ in range(size))

@db.use
def get_user_urls(cursor,user_id):
    query = """SELECT * FROM urls JOIN user_urls ON urls.id = user_urls.url_id WHERE user_urls.user_id = %(user_id)s"""
    cursor.execute( query, {"user_id": user_id} )
    return cursor.fetchall()

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
    query = """INSERT INTO urls (password,url,short_url,views,shortened) VALUES (%(password)s,%(url)s,%(short_url)s,%(views)s,%(shortened)s) RETURNING id"""
    cursor.execute( query, {
        'password': data['password'],
        'url': data['url'],
        'short_url': data['short_url'],
        'views': 0,
        'shortened': 1
    })

    last_insert_id = cursor.fetchone()
    return last_insert_id['id']

@db.use
def add_url_for_user(cursor, data):
    query = """INSERT INTO user_urls (user_id, url_id) VALUES (%(user_id)s,%(url_id)s)"""
    cursor.execute( query, {
        'user_id': data['user_id'],
        'url_id': data['url_id']
    })

@db.use
def delete_user_url(cursor, data):
    query = """DELETE FROM user_urls WHERE user_id = %(user_id)s AND url_id=%(url_id)s"""
    cursor.execute(query, {
        'user_id': data['user_id'],
        'url_id': data['url_id']
    })

def shortify(url, for_user_id=None):
    short_url = ''
    exists = check_if_url_exists(url)

    if exists:
        update_shortened(exists['id'])
        return exists['short_url']

    short_url = generate_random_id(3)

    last_id = add_url({
        'password': '',
        'url': url,
        'short_url': short_url,
        'views': 0,
        'shortened': 0
    })

    if for_user_id is not None:
        add_url_for_user({'url_id': last_id, 'user_id': for_user_id})

    return str(short_url)