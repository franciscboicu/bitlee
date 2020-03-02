from flask import Flask , render_template, redirect, request, url_for, jsonify, session
import test_data_manager as tdm

app = Flask(__name__)

@app.route('/')
def index():
    stuff = tdm.get_everything()
    return jsonify(stuff)

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

@app.route('/shorten-short', methods=['POST'])
def make_short():
    pass

if __name__ == "__main__":
    app.run(
        debug=True,
        host='0.0.0.0'
        )
