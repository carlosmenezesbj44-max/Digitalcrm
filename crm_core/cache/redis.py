import redis
from crm_core.config.settings import settings


class RedisCache:
    def __init__(self):
        self.client = redis.from_url(settings.redis_url)

    def get(self, key: str) -> str:
        return self.client.get(key)

    def set(self, key: str, value: str, expire: int = None):
        self.client.set(key, value, ex=expire)

    def delete(self, key: str):
        self.client.delete(key)

    def exists(self, key: str) -> bool:
        return self.client.exists(key) > 0


redis_cache = RedisCache()
