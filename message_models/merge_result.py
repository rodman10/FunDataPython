import json


class MergeResult(object):

    def __init__(self, pullrequest_id):
        self.pullrequest_id = pullrequest_id

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
