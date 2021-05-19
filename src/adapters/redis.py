import json
import redis

class Redis:
    def __init__(self, endpoint, timeout):
        try:
            self.connection = redis.Redis(
                host=endpoint,
                port=6379,
                db=0,
                socket_timeout=timeout
            )
        except redis.ConnectionError as e:
            print(e)

    def set(self, k, v):
        return self.connection.set(k, json.dumps(v))

    def get(self, k):
        output = self.connection.get(k)
        output = json.loads(output.decode("utf-8")) if output is not None else None
        return output

    def delete(self, k):
        return self.connection.delete(k)
