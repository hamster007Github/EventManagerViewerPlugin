from mapadroid.plugins.endpoints.AbstractPluginEndpoint import AbstractPluginEndpoint
import aiohttp_jinja2

#pluginspecific import
import os
import json
from loguru import logger
#from aiohttp.abc import Request

class Eventlist(AbstractPluginEndpoint):
    """
    "/eventlist"
    """

    # TODO: Auth
    @aiohttp_jinja2.template('event_list.html')
    async def get(self):
        all_events = []
        quest_events = []
        eventManagerStatus = "ok"
        last_update = None
        
        #load cachefile
        try:
            #eventcache_path = "/usr/src/app/plugins/EventManagerViewerPlugin/.eventcache"
            eventcache_path = self.request.config_dict["eventcache_path"]
            f = open(eventcache_path, "r")
            eventcache_dict = json.load(f)
            f.close()
            last_update = eventcache_dict["last_update"]
            for eventdata in eventcache_dict["events"]:
                if "all" in eventdata:
                    all_events = eventdata["all"]
                if "quests" in eventdata:
                    quest_events = eventdata["quests"]
        except Exception as e:
            logger.error(f"EventManagerViewerPlugin: Error while loading eventcachefile")
            logger.exception(e)
            eventManagerStatus = f"ERROR: Can't load data from '{eventcache_path}' file"
        #generate pluginpage
        endpoint_data = {
            "header":"EventManager",
            "title":"Event list",
            "event_list":all_events,
            "quest_list":quest_events,
            "eventManagerStatus":eventManagerStatus,
            "last_update":last_update
        }
        return endpoint_data