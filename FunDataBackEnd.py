from flask import Flask, request, Response, render_template, make_response
from utils.docker_builder import DockerFactory as df
from utils import *
import json
from functools import wraps


def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun



app = Flask(__name__)
docker_factory = df()

@app.route('/')
def hello_world():
    return 'Hello World!'

@allow_cross_domain
@app.route('/terminal', methods=['POST'])
def enter_terminal():
    docker_factory.run_container(1, user_id=int(request.form['user_id']),
                          dataset_id=int(request.form['datasetId']))
    headers = {"Access-Control-Allow-Origin": "*"}
    return Response(json.dumps({'url': 'http://123.207.189.77:8000/jupyter/%s' % str(request.form['user_id'])}),
                    mimetype="application/json", headers=headers)

if __name__ == '__main__':
    app.run()
    mq_client.start_mq_client()

