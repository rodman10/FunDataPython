#coding = utf-8
import pyactivemq
from pyactivemq import ActiveMQConnectionFactory
from message_models.email import email

class MessageListener(pyactivemq.MessageListener):
    def __init__(self, name, queue):
        pyactivemq.MessageListener.__init__(self)
        self.name = name
        self.queue = queue

    def onMessage(self, message):
        self.queue.put('%s got: %s' % (self.name, message.text))

f = ActiveMQConnectionFactory('tcp://123.207.189.77:61616?wireFormat=openwire')
conn = f.createConnection()

nmessages = 100
nconsumers = 3

# create a single producer
producer_session = conn.createSession()
# topic = producer_session.createTopic('topic')
msg_queue = producer_session.createQueue('sample.queue')

producer = producer_session.createProducer(msg_queue)

# create infinite queue that is shared by consumers
# import Queue
# queue = Queue.Queue(0)

# Keep consumers in a list, because if we don'JupyterDockerfile hold a reference to
# the consumer, it is closed
# consumers = []
# for i in xrange(nconsumers):
#     # Create multiple consumers in separate sessions
#     session = conn.createSession()
#     consumer = session.createConsumer(msg_queue)
#     listener = MessageListener('consumer%d' % i, queue)
#     consumer.messageListener = listener
#     consumers.append(consumer)

conn.start()
textMessage = producer_session.createTextMessage()
textMessage.text = email().toJSON()
# textMessage.type = '_type:f'
producer.send(textMessage)
# for i in xrange(nmessages):
#     textMessage.text = email().toJSON()
#     producer.send(textMessage)

# qsize = nmessages * nconsumers
# try:
#     for i in xrange(qsize):
#         message = queue.get(block=True, timeout=5)
#         print message
# except Queue.Empty:
#     raise AssertionError, 'Expected %d messages in queue' % qsize
# assert queue.empty()

conn.close()
