from flask import Flask, render_template, flash, redirect, request, url_for, jsonify, session
from functools import wraps
import test_data_manager as tdm
import user_data_manager as user_dm
import url_data_manager as url_dm

app = Flask(__name__)
app.secret_key = user_dm.random_api_key()
app.config['domain_name'] = 'http://127.0.0.1:5000/'


@app.route("/", defaults={"short_url": None},methods=["GET", "POST"])
@app.route('/<short_url>', methods=["GET", "POST"])
def index(short_url):
    shortified_url_code = ''
    for_user_id = None
    if 'user_id' in session:
        for_user_id = session['user_id']

    if request.method == 'POST':
        if request.form['url'] == '':
            flash('Give Bruce Lee an URL to punch!')
            return render_template('shortner.html')
        shortified_url_code = url_dm.shortify(request.form['url'], for_user_id)

    if short_url == None:
        return render_template('shortner.html', shortified_url_code=shortified_url_code)
        
    url = url_dm.check_if_short_url_exists(short_url)
    if url:
        url_dm.update_views(url['id'])
        return redirect(url['url'])
        
    return render_template('shortner.html', shortified_url_code=shortified_url_code)

@app.route('/account/login', methods=["POST", "GET"])
def account_login():
    if user_dm.is_logged_in():
        return redirect('/')

    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        user = user_dm.check_user(username)
        if user and user_dm.verify_password(password, user['password']):
            session['user_id']   = user['id']
            session['username']  = user['username']
            session['logged_in'] = True
            return redirect('/')
        else: 
            flash('User or Password do not match')

    return render_template('login.html')


@app.route('/account/logout')
def account_logout():
    session.pop('username', None)
    session.pop('user_id', None)
    session.pop('logged_in', None)
    return redirect('/')

@app.route('/account/register', methods=["GET", "POST"])
def account_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['user-password']
        hashed_pass = user_dm.hash_password(password)
        user_dm.add_user(username=username, password=hashed_pass)
        return redirect('/account/login')
    return render_template('register.html', login=False)

@app.route('/account/myurls')
def account_myurls():
    if not user_dm.is_logged_in():
        return redirect('/account/login')
    
    urls = url_dm.get_user_urls(session.get("user_id"))

    return render_template('myurls.html', urls=urls)

@app.route('/account/url/delete', methods=["POST"])
def account_url_delete():
    if not user_dm.is_logged_in():
        return redirect('/account/login')

    if request.method !=  'POST':
        return redirect(url_for("account_myurls"))
    url_id = request.form['url_id']
    url_dm.delete_user_url(url_id)
    return str(url_id)

@app.route('/shorten-short', methods=['POST'])
def make_short():
    short_url = ''
    url = request.form.get('url')
    password = ''

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
