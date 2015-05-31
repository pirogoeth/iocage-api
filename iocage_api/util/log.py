import logging, malibu
from logging import handlers
from malibu.config import configuration

from iocage_api import util


class LoggingDriver(object):

    CONFIG_SECTION = "logging"

    __instance = None

    @staticmethod
    def get_instance():

        if not LoggingDriver.__instance:
            return None

        return LoggingDriver.__instance

    @staticmethod
    def get_logger(name = None):

        if not LoggingDriver.get_instance():
            return None
        
        if name is None:
            name = util.get_caller()

        return LoggingDriver.get_instance().__get_logger(name = name)
    
    def __init__(self, config = {}):
        """ __init__(self, config = {})

            Initializes the logging driver and loads necessary config
            values from the ConfigurationSection that should be passed
            in as config.
        """

        if not isinstance(config, configuration.ConfigurationSection):
            raise TypeError("Config should be of type "
                    "malibu.config.configuration.ConfigurationSection.")
        
        self.__config = config

        self.__logfile = self.__config.get_string("logfile", "/var/log/iocage-api.log")
        self.__loglevel = self.__config.get_string("loglevel", "INFO").upper()
        self.__stream = self.__config.get_bool("console_log", True)

        self.__loglevel = getattr(logging, self.__loglevel, None)
        if not isinstance(self.__loglevel, int):
            raise TypeError("Invalid log level: {}".format(
                self.__config.get_string("loglevel", "INFO").upper()))

        LoggingDriver.__instance = self

        self.__setup_logger()

    def __setup_logger(self):
        """ __setup_logger(self)

            Sets up the logging system with the logfile, loglevel, and
            other streaming options.
        """

        # Set up logging with the root handler so all log objects get the same
        # configuration.
        logger = logging.getLogger("iocage_api")
        logger.setLevel(self.__loglevel)
        formatter = logging.Formatter('%(asctime)s | %(name)-12s %(levelname)-8s: %(message)s')

        file_logger = handlers.RotatingFileHandler(
                self.__logfile,
                maxBytes = 8388608, # 8MB
                backupCount = 4)
        file_logger.setLevel(self.__loglevel)
        file_logger.setFormatter(formatter)

        logger.addHandler(file_logger)

        if self.__stream:
            logger.debug(" --> Building streaming log handler...")
            stream_logger = logging.StreamHandler()
            stream_logger.setLevel(self.__loglevel)
            stream_logger.setFormatter(formatter)

            logger.addHandler(stream_logger)

    def __get_logger(self, name = None):
        """ get_logger(self, name = None)

            Will return a logger object for a specific namespace. 
            If name parameter is None, get_logger will use call
            stack inspection to get the namespace of the last caller.
        """

        if name is None:
            name = util.get_caller()

        return logging.getLogger(name)
