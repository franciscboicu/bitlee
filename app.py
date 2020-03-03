from flask import Flask , render_template, redirect, request, url_for, jsonify, session
import test_data_manager as tdm
import url_data_manager as url_dm
app = Flask(__name__)

@app.route('/')
def index():
    stuff = tdm.get_everything()
    code = url_dm.generate_random_id(3)
    return jsonify(stuff)

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
    url = 'https://facebook.com/'

    #hardcoded for test
    password = request.form.get('password')
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
