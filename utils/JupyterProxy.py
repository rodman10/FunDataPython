import requests

headers = {'Content-Type': 'application/json'}
r = requests.post("http://localhost:8001/api/routes/tt", json={"target":"fds"}, headers = headers)