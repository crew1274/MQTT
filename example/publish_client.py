import logging
import asyncio
from hbmqtt.client import MQTTClient, ConnectException
from hbmqtt.mqtt.constants import *

logger = logging.getLogger(__name__)

@asyncio.coroutine
def test_coro():
    C = MQTTClient()
    yield from C.connect('mqtt://test:test@140.116.39.225:1883')
    tasks = [
        asyncio.ensure_future(C.publish('/test', b'1',qos=QOS_0)),
        asyncio.ensure_future(C.publish('/test', b'2', qos=QOS_1)),
        asyncio.ensure_future(C.publish('/test', b'3', qos=QOS_2)),
    ]
    yield from asyncio.wait(tasks)
    logger.info("messages published")
    yield from C.disconnect()


@asyncio.coroutine
def test_coro2():
    try:
        C = MQTTClient()
        ret = yield from C.connect('mqtt://test:test@140.116.39.225:1883')
        message = yield from C.publish('/test/ncku', b'1', qos=0x00)
        message = yield from C.publish('/test/ncku', b'2', qos=0x01)
        message = yield from C.publish('/test/ncku', b'3', qos=0x02)
        print(message)
        logger.info("messages published")
        yield from C.disconnect()
    except ConnectException as ce:
        logger.error("Connection failed: %s" % ce)
        asyncio.get_event_loop().stop()


if __name__ == '__main__':
    #定義log輸出模式
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    formatter = "%(message)s"
    logging.basicConfig(level=logging.DEBUG, format=formatter, filename='log_publish.txt')

    #執行test_coro(發布訊息)
    asyncio.get_event_loop().run_until_complete(test_coro())
    #asyncio.get_event_loop().run_until_complete(test_coro2())
