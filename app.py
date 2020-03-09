from flask import Flask, render_template, flash, redirect, request, url_for, jsonify, session
import user_data_manager as user_dm
import url_data_manager as url_dm

app = Flask(__name__)
app.secret_key = user_dm.random_api_key()
app.config['domain_name'] = 'http://127.0.0.1:5000/'

@app.route("/",methods=["GET", "POST"])
def index():
    short_url, password = '', ''
    
    if request.method == 'POST' and request.form['url'] == '':
        flash('Give Bruce Lee an URL to punch!')
        return render_template('shortner.html')

    if request.method == 'POST':
        user_id  = session['user_id'] if user_dm.is_logged_in() else None
        password = request.form['password'] if user_dm.is_logged_in() else ''
        short_url = url_dm.shortify(request.form['url'], user_id, password)

    return render_template('shortner.html', shortified_url_code=short_url)

@app.route('/<short_url>', methods=["GET", "POST"])
def unshort_url(short_url=None):    
    url = url_dm.get_url(short_url)

    if request.method == 'POST' and url['password'] is not '':
        if url['password'] == request.form['password']:
            url_dm.update_views(url['id'])
            return redirect(url['url'])
        flash('Hey, wrong password!')       
        return render_template('password_protected_url.html', url=url)

    if url and url['password'] is '':
        url_dm.update_views(url['id'])
        return redirect(url['url'])
    elif url and url['password'] is not '':
        return render_template('password_protected_url.html', url=url)

    flash("What?!")
    return redirect('/')
    
@app.route('/account/login', methods=["POST", "GET"])
def account_login():
    if user_dm.is_logged_in():
        return redirect(url_for('index'))

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
    if user_dm.is_logged_in():
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['user-password']
        hashed_pass = user_dm.hash_password(password)
        user_dm.add_user(username=username, password=hashed_pass)
        flash("Bruce Lee agreed that you can login")
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
    url_dm.delete_user_url({'url_id': url_id, 'user_id': session.get("user_id")})
    return redirect(url_for("account_myurls"))



if __name__ == "__main__":
    app.run(
        debug=True,
        host='0.0.0.0'
    )
