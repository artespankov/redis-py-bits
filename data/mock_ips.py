import redis

ips = ["51.218.112.236", "90.213.45.98", "115.215.230.176", "51.218.112.236"]

if __name__ == "__main__":
    r = redis.Redis(db=5)
    r.delete("ips")
    for ip in ips:
        r.lpush("ips", ip)

    # mock to trigger bot detector
    suspicious_ip = "51.218.112.197"
    for _ in range(20):
        r.lpush("ips", suspicious_ip)
