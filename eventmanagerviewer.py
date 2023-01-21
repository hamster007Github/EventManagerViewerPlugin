import os
import json
from flask import render_template, Blueprint
from mapadroid.madmin.functions import auth_required
import mapadroid.utils.pluginBase


class EventManagerViewerPlugin(mapadroid.utils.pluginBase.Plugin):
    def __init__(self, mad):
        super().__init__(mad)
        self._rootdir = os.path.dirname(os.path.abspath(__file__))
        self._mad = mad
        self._pluginconfig.read(self._rootdir + "/plugin.ini")
        self._local = None
         # add plugin links/pages in madmin only, if plugin is activated by plugin.ini
        if self._pluginconfig.getboolean("plugin", "active", fallback=False):
            self._eventcache_path = self._pluginconfig.get("plugin", "eventcache_path", fallback="") + ".eventcache"
            self._versionconfig.read(self._rootdir + "/version.mpl")
            self.author = self._versionconfig.get("plugin", "author", fallback="hamster007github")
            self.url = self._versionconfig.get("plugin", "url", fallback="https://github.com/ccev/mp-eventwatcher")
            self.description = self._versionconfig.get(
                "plugin", "description", fallback="View EventManager data")
            self.version = self._versionconfig.get("plugin", "version", fallback="1.0")
            self.pluginname = self._versionconfig.get("plugin", "pluginname", fallback="EventManagerViewer")
            self.templatepath = self._rootdir + "/template/"
            self.staticpath = self._rootdir + "/static/"
            self._routes = [("/event_list", self.pluginpage_event_list)]
            self._hotlink = [("Event list", "/event_list", "List current events known by EventManager")]
            # register plugin incl. plugin subpages in madmin
            self._plugin = Blueprint(
                str(self.pluginname), __name__, static_folder=self.staticpath, template_folder=self.templatepath)
            for route, view_func in self._routes:
                self._plugin.add_url_rule(route, route.replace("/", ""), view_func=view_func)
            for name, link, description in self._hotlink:
                self._mad['madmin'].add_plugin_hotlink(name, self._plugin.name+"."+link.replace("/", ""),
                                                       self.pluginname, self.description, self.author, self.url,
                                                       description, self.version)

    def perform_operation(self):
        """The actual implementation of the identity plugin is to just return the
        argument
        """

        # do not change this part ▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽
        if not self._pluginconfig.getboolean("plugin", "active", fallback=False):
            return False
        self._mad['madmin'].register_plugin(self._plugin)
        # do not change this part △△△△△△△△△△△△△△△

        # dont start plugin in config mode
        if self._mad['args'].config_mode:
            return False

    @auth_required
    def pluginpage_event_list(self):
        all_events = []
        quest_events = []
        eventManagerStatus = "ok"
        last_update = None
        #load cachefile
        try:
            f = open(self._eventcache_path, "r")
            eventcache_dict = json.load(f)
            f.close()
            last_update = eventcache_dict["last_update"]
            for eventdata in eventcache_dict["events"]:
                if "all" in eventdata:
                    all_events = eventdata["all"]
                if "quests" in eventdata:
                    quest_events = eventdata["quests"]
        except Exception as e:
            self._mad['logger'].error(f"EventManagerViewerPlugin: Error while loading eventcachefile")
            self._mad['logger'].exception(e)
            eventManagerStatus = f"ERROR: Can't load data from '{self._eventcache_path}' file"
        #generate pluginpage
        try:
            generated_html = render_template("event_list.html", header="EventManager", title="Event list", event_list=all_events, quest_list=quest_events, eventManagerStatus=eventManagerStatus, last_update=last_update)
        except Exception as e:
            self._mad['logger'].error(f"EventManagerViewerPlugin: Error while generating pluginpage 'Event list'")
            self._mad['logger'].exception(e)
        return generated_html

