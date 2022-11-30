# import file
from flask import Flask

application = Flask(__name__)

@application.route('/')
def index():
    pass

if __name__ == '__main__':
    application.run(debug=True)