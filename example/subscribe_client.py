import logging
import asyncio

from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2

logger = logging.getLogger(__name__)

@asyncio.coroutine
def uptime_coro():
    C = MQTTClient()
    yield from C.connect('mqtt://test:test@140.116.39.225:1883')
    yield from C.subscribe([('/test', QOS_1),('/test/ncku', QOS_2)],)
    logger.info("Subscribed")

    try:
        for i in range(1, 100):
            message = yield from C.deliver_message()
            packet = message.publish_packet
            print("%d: %s => %s" % (i, packet.variable_header.topic_name, str(packet.payload.data)))
        yield from C.unsubscribe(['$SYS/broker/uptime', '$SYS/broker/load/#'])
        logger.info("UnSubscribed")
        yield from C.disconnect()
    except ClientException as ce:
        logger.error("Client exception: %s" % ce)


if __name__ == '__main__':
    formatter = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    #執行
    asyncio.get_event_loop().run_until_complete(uptime_coro())