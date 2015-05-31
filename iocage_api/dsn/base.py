import malibu
from malibu import configuration


class BaseDSNDriver(object):
    """ This class represents a bare DSN driver.
        Full DSN management drivers should implement
        this class to install and configure a DSN client
        (such as Sentry's Raven).
    """

    CONFIG_SECTION = "debug"
    SITE_NAME = "iocage-api"

    def __init__(self, app = None):

        self.__app = app
        self.__config = {}
        self.__client = None

        self.__will_run = True
        self.__needs_keys = []

    def set_config(self, config = {}):
        """ set_config(self, config = {})

            Should be provided with a malibu configuration section
            instance to pull config variables from.

            With a Configuration instance, you should do the following:

              driver.set_config(config.get_section(driver.CONFIG_SECTION))
        """

        config_keys = ["enabled", "url", "public_key", "secret_key"]

        for key in config_keys + self.__needs_keys:
            if not self.__will_run: break
            if key not in self.__config:
                print " --> Missing config key: {}".format(key)
                print " --> Please add it to the [debug] section in the config"
                self.__will_run = False
                continue

    def get_config(self):
        """ get_config(self)

            Simply returns this object's configuration section.
        """

        return self.__config

    def get_client(self):
        """ get_client(self)

            Simply returns this object's DSN client instance.
        """

        return self.__client

    def get_app(self):
        """ get_app(self)

            Simply returns this object's app instance.
        """

        return self.__app

    @property
    def enabled(self):
        """ property enabled(self)
            
            Represents the configured status of the DSN.
        """

        return self.__config.get_bool("enabled", True)

    @property
    def url(self):
        """ property url(self)

            Represents the configured DSN url for the driver.
        """

        return self.__config.get_string("url", "")

    @property
    def public_key(self):
        """ property public_key(self)

            Represents the configured public key for connecting
            to the DSN.
        """

        return self.__config.get_string("public_key", "")

    @property
    def secret_key(self):
        """ property secret_key(self)

            Represents the configured secret key for connecting
            to the DSN.
        """

        return self.__config.get_string("secret_key", "")

    def install(self):
        """ install(self)

            Installs the DSN object into the Bottle application to collect
            logs and do the forwarding.
        """

        if not self.__client or not self.__will_run: return False
        else: return True
