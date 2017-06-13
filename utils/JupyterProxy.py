import requests


class JupyterProxy(object):
    def __init__(self):
        self.terminals = []

    def get_terminal(self, user_id, port):
        headers = {'Content-Type': 'application/json'}
        r = requests.post("http://123.207.189.77:8001/api/routes/jupyter/%s" % user_id, json={"target":"http://123.207.189.77:%d" % (port)}, headers = headers)