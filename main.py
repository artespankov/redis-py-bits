import redis
import time
from data.hats import hats
from pprint import pprint
from datetime import timedelta


if __name__ == "__main__":
    # r = redis.Redis(host='localhost', port=6379, db=0, password=None, socket_timeout=None, ...)
    r = redis.Redis(db=1)
    with r.pipeline() as pipe:
        for h_id, hat in hats.items():
            pipe.hmset(h_id, hat)
        pipe.execute()
    r.bgsave()

    keys = r.scan(match="hat:*")[1]
    for key in keys:
        pprint(r.hgetall(key.decode('utf-8')))

    hat_key = keys[0]
    r.hincrby(hat_key, "quantity", -1)
    r.hget(hat_key, "quantity")
    r.hincrby(hat_key, "npurchased", 1)

    # Expiration adn TTL feature
    r.setex(
        "runner",
        timedelta(minutes=1),
        value="catch me if you can"
    )
    #Time to live in seconds
    r.ttl("runner")
    # like ttl, but in ms
    r.pttl("runner")

    r.get("runner")
    r.expire("runner", timedelta(seconds=3))
    time.sleep(3)
    assert r.get('runner') is None
    assert r.exists('runner') == 0

