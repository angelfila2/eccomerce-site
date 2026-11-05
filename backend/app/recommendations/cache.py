import json

from redis.exceptions import RedisError


def cached_recommendations(client, key: str, compute, ttl: int = 60):
    if type(ttl) is not int or ttl <= 0:
        raise ValueError("TTL must be a positive integer")
    try:
        encoded = client.get(key)
        if encoded is not None:
            return json.loads(encoded)
    except (RedisError, ValueError, TypeError, UnicodeDecodeError):
        pass
    result = compute()  # Model/database errors must propagate, unlike cache outages.
    try:
        client.setex(key, ttl, json.dumps(result))
    except RedisError:
        pass
    return result
