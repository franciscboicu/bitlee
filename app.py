from flask import Flask, render_template, redirect, request, url_for, jsonify, session
import test_data_manager as tdm
import user_dm

app = Flask(__name__)
app.secret_key = user_dm.random_api_key()


@app.route('/')
def index():
    stuff = tdm.get_everything()
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


@app.route('/u/<url_hash>')
def unshorten(url):
    pass


@app.route('/my')
def my():
    pass


@app.route('/shorten-short', methods=['POST'])
def make_short():
    pass


if __name__ == "__main__":
    app.run(
        debug=True,
        host='0.0.0.0'
    )
