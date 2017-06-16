import JSONObject
import json
import stomp
from stomp import ConnectionListener
from RedisQueue import RedisQueue as rq
from docker_service import DockerManagement as dm


class TaskListener(ConnectionListener):
    def __init__(self):
        self.r = rq(host='123.206.231.182', port=6379, password='fundata')

    def on_error(self, headers, message):
        print('received an error %s' % message)

    def on_message(self, headers, message):
        print('received a message %s' % message)
        pull_request = json.loads(message, object_hook=JSONObject.JSONObject)
        self.r.put('queue:task', '%s-%s-%s' % (pull_request.fileUrl, pull_request.id, pull_request.datasetId))
        print 'success'


class MergeListener(ConnectionListener):
    def __init__(self):
        self.r = rq(host='123.206.231.182', port=6379, password='fundata')

    def on_error(self, headers, message):
        print('received an error %s' % message)

    def on_message(self, headers, message):
        print('received a message %s' % message)
        merge_request = json.loads(message, object_hook=JSONObject.JSONObject)
        self.r.put('queue:merge', '%s-%s-%s' % (merge_request.newUrl, merge_request.mainUrl, merge_request.datasetId))
        print 'success'




def start_mq_client(c_size=1, j_size=1):
    management = dm(c_size, j_size)
    management.start()
    conns, listeners, queues = [], [TaskListener(), MergeListener()], ['/queue/pullrequest.queue', '/queue/mergerequest.queue']
    for i in range(1):
        conns[i] = stomp.Connection10([('123.207.189.77', 61613)])
        conns[i].set_listener('', listeners[i])
        conns[i].start()
        conns[i].connect()
        conns[i].subscribe(destination=queues[i], id=i, ack='auto')
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