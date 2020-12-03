import datetime
import ipaddress
import redis

blacklist = set()
MAX_VISITS = 15

ip_watcher = redis.Redis(db=5)

while True:
    # blocking method - blocks until new item available on the list
    _, address = ip_watcher.blpop("ips")
    address = ipaddress.ip_address(address.decode("utf-8"))
    now = datetime.datetime.utcnow()
    key = f"{address}:{now.minute}"
    n = ip_watcher.incrby(key, 1)
    if n >= MAX_VISITS:
        print(f"Hat bot detected!:  {address}")
        blacklist.add(address)
    else:
        print(f"{now}:  saw {address}")
    _ = ip_watcher.expire(key, 60)
