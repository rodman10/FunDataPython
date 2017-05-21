import time
import JSONObject
import json
import stomp
import docker

from message_models.email import email
import dockerBuildTest

class MyListener(object):

    def on_error(self, headers, message):
        print('received an error %s' % message)

    def on_message(self, headers, message):
        print('received a message %s' % message)
        pull_request = json.loads(message, object_hook=JSONObject.JSONObject)
        dockerBuildTest.process(pull_request.fileUrl, pull_request.id, pull_request.datasetId)
        print 'success'


def start_mq_client():
    conn = stomp.Connection10([('123.207.189.77', 61613)])
    conn.set_listener('', MyListener())
    conn.start()
    conn.connect()

    conn.subscribe(destination='/queue/pullrequest.queue', id=1, ack='auto')
    #conn.send(body='hello,garfield! this is '.join(sys.argv[1:]), destination='/queue/test')
    # conn.send(body=email().toJSON(), destination='/queue/pullrequest.queue', headers={"_type":"fundata.message.Email"})
    while True:
        pass
# time.sleep(2)
# conn.disconnect()

if __name__ == '__main__':
    start_mq_client()
    # message = '''{"id":4,"datasetId":1,"fileUrl":"http://op9cfw6va.bkt.clouddn.com/o_1bgkf2h161msn7431smnua7a9a7.csv"}'''
    #
    # pull_request = json.loads(message)
    # print pull_request