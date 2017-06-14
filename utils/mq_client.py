import JSONObject
import json
import stomp
from stomp import ConnectionListener
from RedisQueue import RedisQueue as rq
from docker_service import DockerManagement as dm
from docker_builder import DockerFactory as df


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


class JupyterListener(ConnectionListener):
    def __init__(self):
        self.r = rq(host='123.206.231.182', port=6379, password='fundata')
        self.df = df()

    def on_error(self, headers, message):
        print('received an error %s' % message)

    def on_message(self, headers, message):
        print('received a message %s' % message)
        terminal_msg = json.loads(message, object_hook=JSONObject.JSONObject)
        self.df.run_container(1, port=self.df.get_port(), user_id=terminal_msg.user_id, dir="dataset_%s" % terminal_msg.dataset_id)
        # self.r.put('queue:task', '%s-%s' % (terminal_msg.user_id, terminal_msg.dataset_id))
        print 'success'


def start_mq_client(c_size=1, j_size=1):
    management = dm(c_size, j_size)
    management.start()
    conns, listeners, queues = [], [TaskListener(), JupyterListener()], ['/queue/pullrequest.queue', '/queue/terminal.queue']
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