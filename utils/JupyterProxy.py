import requests


class JupyterProxy(object):
    def __init__(self):
        self.terminals = []

    def get_terminal(self):
        headers = {'Content-Type': 'application/json'}
        r = requests.post("http://localhost:8001/api/routes/tt", json={"target":"fds"}, headers = headers)