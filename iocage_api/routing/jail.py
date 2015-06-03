import bottle, json, malibu, zfsapi

from bottle import request, response

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
        except Exception as e:
            yield json.dumps(base.generate_error_response(e))
            raise

        try: iocage = pool.lookup(iocage_conf.get_string("path", "iocage"))
        except Exception as e:
            yield json.dumps(base.generate_error_response(e))
            raise

        try: jails = iocage.lookup("jails")
        except Exception as e:
            yield json.dumps(base.generate_error_response(e))
            raise

        jail_list = [child.name for child in jails.children]

        response = base.generate_bare_response()
        response.update({"jails" : {}})
        
        if "detailed" in request.query:
            for jail in jail_list:
                zjail = jails.lookup(jail)
                jail_dict = {
                        "creation"    : zjail['creation'],
                        "used"        : zjail['used'],
                        "available"   : zjail['available'],
                        "tag"         : zjail['org.freebsd.iocage:tag'],
                        "ip4_addr"    : zjail['org.freebsd.iocage:ip4_addr'],
                        "ip6_addr"    : zjail['org.freebsd.iocage:ip6_addr']
                }
                response["jails"].update({jail : jail_dict})
        else:
            response["jails"] = jail_list

        yield json.dumps(response)

register_route_providers = [JailAPIRouter]
