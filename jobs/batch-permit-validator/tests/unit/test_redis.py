import redis
from testcontainers.redis import RedisContainer


def test_redis_connection():
    """Check the simple container starts and stops automatically."""
    with RedisContainer(image="redis:latest") as redis_container:
        # Get the connection client, which uses mapped ports to connect reliably
        redis_client: redis.Redis = redis_container.get_client()

        # Perform Redis operations
        key = "test_key"
        expected_value = "Hello, Testcontainers!"
        redis_client.set(key, expected_value)
        actual_value = redis_client.get(key).decode("utf-8")

        assert actual_value == expected_value
