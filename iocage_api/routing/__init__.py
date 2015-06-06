import glob, importlib, os
from importlib import import_module

from iocage_api.routing import base
from iocage_api.util import log
modules = glob.glob(os.path.dirname(__file__) + "/*.py")
__all__ = [os.path.basename(f)[:-3] for f in modules if not os.path.basename(f).startswith('_') and not f.endswith('__init__.py') and os.path.isfile(f)]


def load_routing_modules(manager):

    providers = []

    logger = log.LoggingDriver.get_logger()
    
    logger.debug("Searching %s for routing providers.." % (__all__))
    
    for module in __all__:
        module = import_module("{}.{}".format(__package__, module))
        if not hasattr(module, "register_route_providers"):
            continue
        for rtcls in module.register_route_providers:
            logger.debug("Found provider %s in module %s" % (
                rtcls.__name__, module.__name__))
            providers.append(rtcls)
        # Type validation
    
    return [provider(manager) for provider in providers]
