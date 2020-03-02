from flask import Flask , render_template, redirect, request, url_for, jsonify, session
import test_data_manager as tdm
import url_data_manager as url_dm
app = Flask(__name__)

@app.route('/')
def index():
    stuff = tdm.get_everything()
    code = url_dm.generate_random_id(3)
    urls = url_dm.get_url_by_shorten(code)
    return jsonify(urls)

@app.route('/account/login', methods=["POST"])
def account_login():
    pass

@app.route('/account/register', methods=["POST"])
def account_register():
    pass

@app.route('/u/<url_hash>')
def unshorten(url):
    pass

@app.route('/my')
def my():
    pass

@app.route('/shorten-short', methods=['GET'])
def make_short():
    short_url = ''
    url = request.form.get('url')
    password = request.form.get('password')
    exists = url_dm.check_if_short_url_exists(url)

    if exists[0] == True:
        url = exists[1]
        id = url['id']
        url_dm.update_views(url['id'])

        return redirect(url['url'])
    
    return 'Does not exist'


if __name__ == "__main__":
    app.run(
        debug=True,
        host='0.0.0.0'
        )
