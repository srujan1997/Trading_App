import os
import redis


def get_redis_connection():
    redis_conn = redis.StrictRedis(
        host=os.environ.get("CACHE_URL", "redis"),
        port=6379,
        db=0,
        password=os.environ.get("CACHE_PASSWORD", ""),
        socket_timeout=2,
        socket_connect_timeout=2,
    )

    return redis_conn


def get_from_redis(key):
    redis_conn = get_redis_connection()
    if redis_conn:
        value = redis_conn.get(key)
        if value:
            value = value.decode("utf-8")
    return value


def set_in_redis(key, value, expiry=None):
    redis_conn = get_redis_connection()
    if redis_conn:
        if expiry is None:
            expiry = 1 * 60 * 60
        redis_conn.setex(key, expiry, value)
        return value
