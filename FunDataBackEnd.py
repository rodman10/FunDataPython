from flask import Flask
from utils import *
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    mq_client.start_mq_client()
    app.run()
