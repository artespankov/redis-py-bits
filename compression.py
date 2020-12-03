import bz2
import redis

if __name__ == "__main__":
    r = redis.Redis()

    blob = "I have a lot to talk about" * 1000
    l1 = len(blob.encode("utf-8"))
    print(l1)

    r.set("sg:500", bz2.compress(blob.encode("utf-8")))
    l2 = len(r.get("sg:500"))
    print(l2)

    # Magnitude of savings
    print(l1 / l2)

    decompressed_blob = bz2.decompress(r.get("sg:500")).decode("utf-8")
    assert decompressed_blob == blob
