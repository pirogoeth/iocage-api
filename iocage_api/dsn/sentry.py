import malibu, raven
from raven.contrib.bottle import Sentry
from malibu import configuration

from iocage_api.dsn import base


class SentryDSNDriver(base.BaseDSNDriver):

    def __init__(self, app = None):

        BaseDSNDriver.__init__(self, app)

        self.__wrapper = None

        self.__needs_keys = ["project_id"]

    def get_bottle_wrapper(self):
        """ get_bottle_wrapper(self)

            Returns the Sentry wrapper used to wrap the Bottle app
            for exception catching.
        """

        return self.__wrapper

    @property
    def project_id(self):
        """ property project_id(self)

            Represents the configured project id to log events 
            to in the DSN.
        """

        return self.__config.get_int("project_id", -1)

    def install(self):
        """ insert(self)

            Instantiates and installs the Raven DSN into the Bottle
            framework for error reporting to Sentry.
        """

        site_name = super(SentryDSNDriver, self).SITE_NAME
        
        if not super(SentryDSNDriver, self).install():
            return False
        
        try:
            self.__client = raven.Client(
                    dsn = self.url,
                    public_key = self.public_key,
                    secret_key = self.private_key,
                    project = self.project_id,
                    site_name = site_name)

            self.__app.catchall = False
            self.__wrapper = Sentry(self.__app, self.__client)
        except Exception as e:
            print " --> Encountered Exception while setting up DSN:"
            print " --> {}".format(e)
            return False

        return True
