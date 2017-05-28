import redis


class RedisQueue(object):
    def __init__(self, **kwargs):
        self.r = redis.StrictRedis(**kwargs)

    def put(self, key, message):
        self.r.rpush(key, message)

    def get(self, key, block=True, timeout=None):
        if block:
            item = self.r.blpop(key, timeout=timeout)
        else:
            item = self.r.lpop(key)
        if item:
            item = item[1]
        return str(item)