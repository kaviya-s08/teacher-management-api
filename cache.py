
import redis

# Connect to local Redis server
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True,
    socket_connect_timeout=3
)

# Check Redis connection
def test_redis_connection():
    return redis_client.ping()
