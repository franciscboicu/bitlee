from flask import Flask, render_template, redirect, request, url_for, jsonify, session
import test_data_manager as tdm
import user_dm
import url_data_manager as url_dm

app = Flask(__name__)
app.secret_key = user_dm.random_api_key()


@app.route('/')
def index():
    stuff = tdm.get_everything()
    code = url_dm.generate_random_id(3)
    return jsonify(stuff)


@app.route('/account/login', methods=["POST", "GET"])
def account_login():
    login = True
    logged_in = False
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['user-password']
        hashed_pass = user_dm.check_user(username)
        if user_dm.verify_password(password, hashed_pass['password']):
            session['username'] = hashed_pass['id']
            logged_in = True
        return render_template('index.html', logged_in=logged_in)
    return render_template('index.html', login=login)


@app.route('/account/logout')
def account_logout():
    session.pop('username', None)
    return render_template('url_index.html')


@app.route('/account/register', methods=["GET", "POST"])
def account_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['user-password']
        hashed_pass = user_dm.hash_password(password)
        user_dm.add_user(username=username, password=hashed_pass)
    return render_template('index.html', login=False)



@app.route('/u/<short_url>')
def unshorten(short_url):
    url = url_dm.check_if_short_url_exists(short_url)
    if url:
        url_dm.update_views(url['id'])
        return redirect(url['url'])
    return '404'

@app.route('/my')
def my():
    pass


@app.route('/shorten-short', methods=['GET'])
def make_short():
    short_url = ''

    #hardcoded for test
    url = request.form.get('url')
    #url = 'https://facebook.com/'

    #hardcoded for test
    password = request.form.get('password')
    #password = ''

    exists = url_dm.check_if_url_exists(url)

    if exists:
        url_dm.update_shortened(exists['id'])
        return exists['short_url'] + " Already exists"

    short_url = url_dm.generate_random_id(3)
    url_dm.add_url({
        'password': password,
        'url': url,
        'short_url': short_url,
        'views': 0,
        'shortened': 0
    })
    return str(short_url) + " Inserted as new"


if __name__ == "__main__":
    app.run(
        debug=True,
        host='0.0.0.0'
    )
