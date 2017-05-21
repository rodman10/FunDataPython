import json


class email(object):

    def __init__(self):
        self.to, self.body, self._type = "1@2", "haha", "fundata.message.Email"

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
