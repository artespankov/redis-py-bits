import logging
import redis

logging.basicConfig()


class OutOfStockError(Exception):
    """Raised when PyHats is all out of today's hottest hat"""


def buy_item(r: redis.Redis, item_id: int) -> None:
    """ Triggers an error if watched item was touched in between of operations and re-run next try.
        This is the “optimistic” part of the locking: rather than letting the client have a time-consuming total lock
        on the database through the getting and setting operations, leave it up to Redis to notify the client and user
        only in the case that calls for a retry of the inventory check. """
    with r.pipeline() as pipe:
        error_count = 0
        while True:
            try:
                # Get available inventory, watching for changes
                # related to this item_id before the transaction
                pipe.watch(item_id)
                num_left: bytes = r.hget(item_id, "quantity")
                if int(num_left) > 0:
                    pipe.multi()
                    pipe.hincrby(item_id, "quantity", -1)
                    pipe.hincby(item_id, "npurchased", 1)
                    pipe.execute()
                    break
                else:
                    # Stop watching the item_id and raise to break out
                    pipe.unwatch()
                    raise OutOfStockError(f"Sorry, {item_id} is out of stock!")
            except redis.WatchError:
                # Log total number of errors by this user to buy this item,
                # then try the same process again of WATCH/HGET/MULTI/EXEC
                error_count += 1
                logging.warning(f"WatchError {item_id}: {error_count}; retrying")
