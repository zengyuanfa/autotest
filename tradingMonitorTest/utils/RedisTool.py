import redis
import json

class RedisUtil:
    def __init__(self, host='localhost', port=6379, db=0, password=None):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db, password=self.password)
        self.redis= redis.Redis(connection_pool=pool)

    def set(self, key, value, expire=None):
        self.redis.set(key, value)
        if expire:
            self.redis.expire(key, expire)

    def get(self, key):
        return self.redis.get(key)

    def delete(self, key):
        self.redis.delete(key)

    def exist(self, key):
        return self.redis.exists(key)

    def hset(self, name, key, value):
        self.redis.hset(name, key, value)

    def hget(self, name, key):
        return self.redis.hget(name, key)

    def hmset(self, name, mapping):
        self.redis.hmset(name, mapping)

    def hmget(self, name, keys):
        return self.redis.hmget(name, keys)

    def hgetall(self, name):
        return self.redis.hgetall(name)

    def hkeys(self, name):
        return self.redis.hkeys(name)

    def hlen(self, name):
        return self.redis.hlen(name)

    def hdel(self, name, key):
        self.redis.hdel(name, key)

    def set_dict(self, key, value):
        """将字典类型的数据存入redis"""
        value_str = json.dumps(value)
        self.redis.set(key, value_str)

    def get_dict(self, key):
        """从redis中取出字典类型的数据"""
        value_str = self.redis.get(key)
        if value_str is not None:
            return json.loads(value_str)
        else:
            return None

    def publish(self, channel, message):
        self.redis.publish(channel, message)

    def subscribe(self, channel):
        pubsub = self.redis.pubsub()
        pubsub.subscribe(channel)
        return pubsub

if __name__ == "__main__":
    redis = RedisUtil(host='host', password='password')
    test_dict = {'buy': 5, 'sell': 25, 'net_buy': -20, 'total': 30}
    redis.set_dict('test_dict', test_dict)
    val = redis.get_dict('test_dict')
    print(val)
