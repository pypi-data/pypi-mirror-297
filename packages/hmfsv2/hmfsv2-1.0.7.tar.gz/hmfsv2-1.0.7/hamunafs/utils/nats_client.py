import orjson
import asyncio
import nats
from nats.errors import ConnectionClosedError, TimeoutError, NoServersError
from hamunafs.utils.singleton_wrapper import Singleton

class NATSClient(Singleton):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def connect(self):
        self.client = await nats.connect('nats://{}:{}'.format(self.host, self.port))

    async def publish(self, topic, params):
        if isinstance(params, str):
            _params = params.encode()
        else:
            _params = orjson.dumps(params)
        await self.client.publish(topic, _params)
