import logging
import asyncio
import os
from hbmqtt.utils import read_yaml_config
from hbmqtt.broker import Broker
logger = logging.getLogger(__name__)
config = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'bind': '0.0.0.0:1883',
            'max-connections': 50000,
        },
        'websocket': {
            'type': 'ws',
            'bind': '0.0.0.0:1884',
            'max-connections': 50000,
        },
    },
    'sys_interval': 10,
    'auth': {
        'allow-anonymous': True,
        'password-file': os.path.join(os.path.dirname(os.path.realpath(__file__)), "list"),
        'plugins': ['auth_file', 'auth_anonymous']
    }
}
config = read_yaml_config(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.yaml'))
logger.debug("Using default configuration")
broker = Broker(config)
@asyncio.coroutine
def coro():
    yield from broker.start()
if __name__ == '__main__':
    #定義log輸出模式
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.get_event_loop().run_until_complete(coro())
    asyncio.get_event_loop().run_forever()