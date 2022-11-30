# import file
from flask import Flask

application = Flask(__name__)

@application.route('/')
def index():
    pass

@application.route('/register')
def register():
    pass

@application.route('/save_data_register')
def save_data_register():
    pass

@application.route('/login')
def login():
    pass

@application.route('/login_verification')
def login_verification():
    pass

@application.route('/add_transaction')
def add_transaction():
    pass

if __name__ == '__main__':
    application.run(debug=True)