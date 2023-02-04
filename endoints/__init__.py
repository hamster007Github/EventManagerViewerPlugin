from aiohttp import web
from plugins.EventManagerViewerPlugin.endoints.Eventlist import Eventlist

def register_custom_plugin_endpoints(app: web.Application):
    app.router.add_view('/eventlist', Eventlist, name='eventlist')
