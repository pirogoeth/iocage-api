import malibu, sys, traceback
from malibu.config import configuration
from malibu.util import log


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


def generate_bare_response():
    """ generate_bare_response()

        Generates a bare, generic "good" response.
    """

    response = {"status" : 200}

    return response


def generate_error_response(exception = None):
    """ generate_error_response(exception = None)

        Generates a dictionary with error codes and exception information
        to return instead of a bland, empty dictionary.

        If exception is not provided, this method will return exception
        information based on the contents of sys.last_traceback
    """

    response = {"status" : 500, "stacktrace" : {}}

    traceback_pos = 0
    for trace in traceback.extract_tb(sys.exc_info[2], 4):
        response['stacktrace'].update({traceback_pos : ' '.join(trace)})
        traceback_pos += 1

    if exception:
        response.update({"exception" : str(exception)})

    return response


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
