"""
Usage:
    python3 broker_script.py --version
    python3 broker_script.py (-h | --help)
    python3 broker_script.py [-c <config_file> ] [-d]

Options:
    -c <config_file>    Broker configuration file (YAML format)
    -d                  Enable debug messages
"""

import sys
import logging
import asyncio
import os
from hbmqtt.broker import Broker
from hbmqtt.version import get_version
from docopt import docopt
from hbmqtt.utils import read_yaml_config


default_config = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'bind': '0.0.0.0:1883',
        },
    },
    'sys_interval': 10,
    'auth': {
        'allow-anonymous': True,
        'password-file': os.path.join(os.path.dirname(os.path.realpath(__file__)), "passwd"),
        'plugins': [
            'auth_file', 'auth_anonymous'
        ]
    }
}

logger = logging.getLogger(__name__)


def main(*args, **kwargs):

    #檢查python版本，必須3.4之後
    if sys.version_info[:2] < (3, 4):
        logger.fatal("Error: Python 3.4+ is required")
        sys.exit(-1)

    arguments = docopt(__doc__, version=get_version())
    formatter = "[%(asctime)s] :: %(levelname)s - %(message)s"

    #debug mode
    if arguments['-d']:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(level=level, format=formatter)

    config = None
    if arguments['-c']:
        config = read_yaml_config(arguments['-c'])
    else:
        config = read_yaml_config(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'default_broker.yaml'))
        logger.debug("Using default configuration")
    
    loop = asyncio.get_event_loop()
    #啟動broker
    broker = Broker(config)
    try:
        loop.run_until_complete(broker.start())
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(broker.shutdown())
    finally:
        loop.close()


if __name__ == "__main__":
    main()