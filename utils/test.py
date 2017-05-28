import redis

r = redis.StrictRedis(host='123.206.231.182', port=6379, password='fundata')
key = 'queue:task'
r.rpush(key, '%s-%s-%s' % (u'o_1bgkh3g1n194p13dmrov1m6437j7.csv'.encode('utf-8'), 4 ,1))