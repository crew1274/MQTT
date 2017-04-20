import logging
import asyncio
import os
from hbmqtt.broker import Broker

logger = logging.getLogger(__name__)

config = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'bind': '0.0.0.0:1883',
            'max-connections': 50000,
        },
        'ws-mqtt': {
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

broker = Broker(config)

@asyncio.coroutine
def test_coro():
    yield from broker.start()
    #yield from asyncio.sleep(5)
    #yield from broker.shutdown()


if __name__ == '__main__':
    #定義log輸出模式
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    #formatter = "%(asctime)s :: %(levelname)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    #紀錄log
    logging.basicConfig(level=logging.DEBUG, format=formatter, filename='log-broker.txt')

    asyncio.get_event_loop().run_until_complete(test_coro())
    asyncio.get_event_loop().run_forever()