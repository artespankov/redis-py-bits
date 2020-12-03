import json
import redis
from cryptography.fernet import Fernet

if __name__ == "__main__":
    r = redis.Redis()

    cipher = Fernet(Fernet.generate_key())
    info = {
        "cardnum": 2211849528391929,
        "exp": [2020, 9],
        "cv2": 842
    }

    r.set(
        "user:1000",
        cipher.encrypt(json.dumps(info).encode("utf-8"))
    )

    print(r.get("user:1000"))

    print(cipher.decrypt(r.get("user:1000")))

    print(json.loads(cipher.decrypt(r.get("user:1000"))))
