import bottle, iocage_api, malibu, sys

from bottle import Bottle, redirect, request, route, run

from malibu.config import configuration
from malibu.util import args, log

from iocage_api import dsn, routing, util


class IOCageAPIManager(object):

    __instance = None

    @classmethod
    def get_instance(cls):

        return cls.__instance
    
    def __init__(self):
        """ __init__(self)

            Initializes variables for config, begins config read,
            launches the DSN driver and sets up logging. After all that,
            launches the bottle server.
        """

        self.__config = configuration.Configuration()
        self.__app = None
        self.__dsn = None
        self.__logger = None

        self.__args = args.ArgumentParser.from_argv()
        self.__args.add_option_mapping('c', 'config')
        self.__args.set_default_param_type('config', 
                opt = args.ArgumentParser.OPTION_PARAMETERIZED)
        self.__args.parse()

        try: self.__config_file = self.__args.options['config']
        except: self.__config_file = "api.ini"

        try: self.__config.load(self.__config_file)
        except:
            raise # XXX - Handle this properly.

        IOCageAPIManager.__instance = self

    def load_bottle(self):
        """ load_bottle(self)

            Loads the bottle server and stores it.
        """

        self.__app = Bottle()
        if self.__config.get_section("debug").get_bool("enabled", False):
            self.__app.catchall = False
            bottle.debug(True)
        
        return self.__app

    def load_dsn(self):
        """ load_dsn(self)

            Loads the DSN driver and stores it.
        """

        dsn_enable = self.__config.get_section("debug").get_bool("enabled", False)
        if not dsn_enable:
            return None

        dsn_config = self.__config.get_section("debug")
        dsn_class = dsn.load_dsn(dsn_config.get_string("dsn_type", "sentry"))
        if not dsn_class:
            return None

        self.__dsn = dsn_class(self.__app)
        self.__dsn.set_config(config = dsn_config)
        self.__dsn.install()

        return self.__dsn

    def load_logging(self):
        """ load_logging(self)

            Loads the logging driver and stores it.
        """

        logging_config = self.__config.get_section("logging")

        logging_inst = log.LoggingDriver(config = logging_config)
        self.__logger = logging_inst

        return logging_inst.get_logger(name = "iocage_api")

    def run_bottle(self):
        """ run_bottle(self)

            Actually runs the bottle server for the API.
        """

        if not self.__app:
            return Exception("Bottle server has not been instantiated.")

        bottle_config = self.__config.get_section("api")

        if self.__dsn:
            run(
                    app = self.__dsn.get_bottle_wrapper(),
                    host = bottle_config.get_string("listen", "127.0.0.1"),
                    port = bottle_config.get_int("port", 18040),
                    quiet = False,
                    debug = True)
            return

    @property
    def app(self):
        """ property app(self)

            Return app instance.
        """

        return self.__app
    
    @property
    def config(self):
        """ property config(self)

            Return config instance.
        """

        return self.__config

    @property
    def dsn(self):
        """ property dsn(self)

            Return DSN instance.
        """

        return self.__dsn

