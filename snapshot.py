# There are 2 ways to enable snapshotting in Redis

# 1. Via config option
# /etc/redis/6379.conf
# ....
# dbfilename        dump.rdb
# dir               ./
# rdbcompression    yes


# 2. Manually with redis-cli/redis-py commands
# 127.0.0.1:6379> BGSAVE
# <Background saving started

# check a dump file
# $ file -b dump.rdb

if __name__ == "__main__":
    import redis
    r = redis.Redis()
    print(r.lastsave())
    r.bgsave()
    print(r.lastsave())
