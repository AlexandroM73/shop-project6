import fakeredis
from django.core.cache.backends.base import BaseCache

class FakeRedisCache(BaseCache):
    def __init__(self, server, params):
        super().__init__(params)
        # fakeredis.FakeServer() — это и есть наш «поддельный» Redis
        self._server = fakeredis.FakeServer()
        self.client = fakeredis.FakeStrictRedis(server=self._server)

    def get(self, key, default=None, version=None):
        key = self.make_key(key, version=version)
        value = self.client.get(key)
        if value is None:
            return default
        return value

    def set(self, key, value, timeout=None, version=None, client=None):
        key = self.make_key(key, version=version)
        if timeout is None:
            timeout = self.default_timeout
        self.client.setex(key, int(timeout), value)

    def delete(self, key, version=None):
        key = self.make_key(key, version=version)
        self.client.delete(key)

    def clear(self):
        self.client.flushdb()
