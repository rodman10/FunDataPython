import JSONObject
import json
import stomp
from stomp import ConnectionListener
from RedisQueue import RedisQueue as rq
from docker_service import DockerManagement as dm
from message_models.merge_result import MergeResult


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
        self.r.put('queue:merge', '%s-%s-%s-%s' % (merge_request.newUrl, merge_request.mainUrl, merge_request.datasetId, merge_request.pullRequestId))
        print 'success'


def start_mq_client(c_size=1, m_size=1):
    management = dm(c_size, m_size)
    management.start()
    sub_conns, listeners, sub_queues = [], [TaskListener(), MergeListener()], ['/queue/pullrequest.queue', '/queue/mergerequest.queue']
    for i in range(len(sub_queues)):
        sub_conns.append(stomp.Connection10([('123.207.189.77', 61613)]))
        sub_conns[i].set_listener('', listeners[i])
        sub_conns[i].start()
        sub_conns[i].connect()
        sub_conns[i].subscribe(destination=sub_queues[i], id=i, ack='auto')

    pub_conns, pub_queues = [], ['/queue/mergeresult.queue']
    for i in range(len(pub_queues)):
        pub_conns.append(stomp.Connection10([('123.207.189.77', 61613)]))
        pub_conns[i].start()
        pub_conns[i].connect()

    r = rq(host='123.206.231.182', port=6379, password='fundata')
    for item in r.listen('queue:merge_result'):
        pub_conns[0].send(body=MergeResult(int(item)).toJSON(), destination=pub_queues[0], headers={"_type":"fundata.message.ResultMessage"})
    # pub_conns[0].send(body=MergeResult(int("1")).toJSON(), destination=pub_queues[0], headers={"_type":"fundata.message.ResultMessage"})

    #conn.send(body='hello,garfield! this is '.join(sys.argv[1:]), destination='/queue/test')


if __name__ == '__main__':
    start_mq_client()
    # message = '''{"id":4,"datasetId":1,"fileUrl":"http://op9cfw6va.bkt.clouddn.com/o_1bgkf2h161msn7431smnua7a9a7.csv"}'''
    #
    # pull_request = json.loads(message)
    # print pull_request