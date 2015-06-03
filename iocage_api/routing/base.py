import malibu
from malibu.config import configuration

from iocage_api.util import log


def api_route(path = "", actions = []):
    """ decorator api_route(path = "", actions = [])

        Sets values on route functions to automate 
        loading routes into Bottle.
    """

    def api_route_outer(route_function):
        
        setattr(route_function, "route_func", True)
        setattr(route_function, "path", path)
        setattr(route_function, "actions", actions)

        return staticmethod(route_function)
    return api_route_outer


class APIRouter(object):

    def __init__(self, manager):

        self.__log = log.LoggingDriver.get_logger()
        
        self.manager = manager
        self.app = self.manager.app

        self.routes = self.load_routes()

    def load_routes(self):
        """ load_routes(self)

            Loads route functions into Bottle based on the presence of
            extra variables in a function object.
        """

        routes = []

        for member in dir(self):
            member = getattr(self, member)
            if member and hasattr(member, "route_func"):
                self.__log.debug("Found routing function %s" % (member.__name__))
                routes.append(member)

        for route in routes:
            self.__log.debug("Routing %s requests to %s for path -> %s" % (
                    route.actions, route.path, route.__name__))
            self.app.route(route.path, route.actions, route)

        return routes
