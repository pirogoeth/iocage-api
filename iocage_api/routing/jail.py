import json, malibu, zfsapi

from iocage_api import manager
from iocage_api.routing import base
from iocage_api.routing.base import api_route

from malibu.config import configuration

from zfsapi.connection import ZFSConnection

class JailAPIRouter(base.APIRouter):

    def __init__(self, manager):

        base.APIRouter.__init__(self, manager)

    @api_route(path = "/jails", actions = ["GET"])
    def list_jails():
        """ GET /jails

            Returns a list of jail UUIDs.
        """

        config = manager.IOCageAPIManager.get_instance().config

        iocage_conf = config.get_section("iocage")
        zfs = ZFSConnection()
        zfs.load_properties(zfs.pools)

        try: pool = zfs.pools.lookup(iocage_conf.get_string("zfs_pool", "root"))
        except:
            yield json.dumps({})
            raise

        try: iocage = pool.lookup(iocage_conf.get_string("path", "iocage"))
        except:
            yield json.dumps({})
            raise

        try: jails = iocage.lookup("jails")
        except:
            yield json.dumps({})
            raise

        jail_list = [child.name for child in jails.children]

        yield json.dumps(jail_list)

register_route_providers = [JailAPIRouter]
