#!/usr/bin/env python2.7

from iocage_api import routing, manager, util
from iocage_api.manager import IOCageAPIManager
from iocage_api.util import log


if __name__ == '__main__':

    manager = IOCageAPIManager()
    manager.load_logging()
    log = log.LoggingDriver.get_logger(name = "iocage_api.__main__")
    log.info(" --> Loading Bottle server...")
    manager.load_bottle()
    log.info(" --> Loading API routes...")
    routing.load_routing_modules(manager)
    log.info(" --> Loading DSN driver...")
    manager.load_dsn()
    log.info(" --> Running Bottle server!")
    try:
        manager.run_bottle()
    except:
        manager.dsn.client.captureException()
