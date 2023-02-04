# general plugin imports
import os
from typing import Dict
from aiohttp import web
import mapadroid.plugins.pluginBase
from plugins.EventManagerViewerPlugin.endoints import register_custom_plugin_endpoints

class EventManagerViewerPlugin(mapadroid.plugins.pluginBase.Plugin):
    """This plugin is just the identity function: it returns the argument
    """

    def _file_path(self) -> str:
        return os.path.dirname(os.path.abspath(__file__))

    def __init__(self, subapp_to_register_to: web.Application, mad_parts: Dict):
        super().__init__(subapp_to_register_to, mad_parts)

        # add plugin links/pages in madmin only, if plugin is activated by plugin.ini
        if self._pluginconfig.getboolean("plugin", "active", fallback=False):
            register_custom_plugin_endpoints(self._plugin_subapp)
            self._hotlink = [("Event list", "eventlist", "List current events known by EventManager")]
            for name, link, description in self._hotlink:
                self._mad_parts['madmin'].add_plugin_hotlink(name, link.replace("/", ""),
                                                       self.pluginname, self.description, self.author, self.url,
                                                       description, self.version)
            self._plugin_subapp["eventcache_path"] = self._pluginconfig.get("plugin", "eventcache_path", fallback="") + ".eventcache"

    async def _perform_operation(self):
        # nothing cyclically to do -> directly return
        return True