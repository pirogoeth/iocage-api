import malibu, raven
from raven.contrib.bottle import Sentry
from malibu import configuration

from iocage_api.dsn import base
from iocage_api.util import log


class SentryDSNDriver(base.BaseDSNDriver):

    def __init__(self, app = None):

        base.BaseDSNDriver.__init__(self, app = app)

        self.__base = super(SentryDSNDriver, self)
        self.__wrapper = None
        self.__logger = log.LoggingDriver.get_logger()

        self.__needs_keys = ["project_id"]

    def set_config(self, config = {}):
        """ set_config(self)

            Wrapper for BaseDSNDriver.set_config() to connect the Sentry
            DSN client immediately after the config is verified.
        """

        self.__base.set_config(config = config)

        if len(self.__base.get_config()) > 0:
            self.__config = config

        if self.will_run:
            self.connect()

    def get_bottle_wrapper(self):
        """ get_bottle_wrapper(self)

            Returns the Sentry wrapper used to wrap the Bottle app
            for exception catching.
        """

        return self.__wrapper

    def connect(self):
        """ connect(self)

            Connects the DSN client to the DSN itself and returns the
            instance.
        """

        site_name = self.__base.SITE_NAME
        
        try:
            self.__client = raven.Client(
                    dsn = self.__base.url,
                    public_key = self.__base.public_key,
                    secret_key = self.__base.secret_key,
                    project = self.project_id,
                    site_name = site_name)
            self.__base.set_client(self.__client)
            self.__logger.info("Connected to Sentry DSN.")
        except Exception as e:
            self.__will_run = False
            self.__logger.error(" --> Encountered Exception while connecting DSN:")
            self.__logger.error(" --> {}".format(e))
            return None

        return self.__client

    def install(self):
        """ install(self)

            Instantiates and installs the Raven DSN into the Bottle
            framework for error reporting to Sentry.
        """

        if not self.__base.install():
            return False
        
        try:
            self.__base.get_app().catchall = False
            self.__wrapper = Sentry(self.__base.get_app(), self.__client)
        except Exception as e:
            self.__logger.error(" --> Encountered Exception while installing DSN:")
            self.__logger.error(" --> {}".format(e))
            return False

        return True
    
    @property
    def project_id(self):
        """ property project_id(self)

            Represents the configured project id to log events 
            to in the DSN.
        """

        return self.__config.get_int("project_id", -1)

    @property
    def client(self):
        """ property client(base)

            Represents the client instance that is stored
            somewhere between self and base because of 
            subclassing.
        """

        return self.__base.get_client()
