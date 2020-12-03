import json
import redis
from pprint import pprint


if __name__ == "__main__":
    restaurant_id = 484272

    restaurant_484272 = {
        "name": "Ravagh",
        "type": "Persian",
        "address": {
            "street": {
                "line1": "11 E 30th St",
                "line2": "APT 1",
            },
            "city": "New York",
            "state": "NY",
            "zip": 10016,
        }
    }

    r = redis.Redis()
    r.set(restaurant_id, json.dumps(restaurant_484272))

    pprint(json.loads(r.get(restaurant_id)))
