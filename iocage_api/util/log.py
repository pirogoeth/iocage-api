import logging, malibu
from malibu.config import configuration
from iocage_api import util

class LoggingDriver(object):

    __instance = None

    @staticmethod
    def get_instance():

        if not LoggingDriver.__instance:
            return None

        return LoggingDriver.__instance

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
        self.__stream = self.__config.get_boolean("console_log", True)

        self.__loglevel = getattr(logging, self.__loglevel, None)
        if not isinstance(self.__loglevel, int):
            raise TypeError("Invalid log level: {}".format(
                self.__config.get_string("loglevel", "INFO").upper()))

        self.__setup_logger()

    def __setup_logger(self):
        """ __setup_logger(self)

            Sets up the logging system with the logfile, loglevel, and
            other streaming options.
        """

        logger = logging.getLogger(__name__)

        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')

        file_logger = logging.RotatingFileHandler(
                self.__logfile,
                maxBytes = 8388608, # 8MB
                backupCount = 4)
        file_logger.setLevel(self.__loglevel)
        file_logger.setFormatter(formatter)

        logger.addHandler(file_logger)

        if self.__stream:
            stream_logger = logging.StreamHandler()
            stream_logger.setLevel(self.__loglevel)
            stream_logger.setFormatter(formatter)

            logger.addHandler(stream_logger)

    def get_logger(self, name = None):
        """ get_logger(self, name = None)

            Will return a logger object for a specific namespace. 
            If name parameter is None, get_logger will use call
            stack inspection to get the namespace of the last caller.
        """

        if name is None:
            name = util.get_caller()

        return logging.getLogger(name)
