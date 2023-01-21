# Development
This plugin just visuallize events from standalone [EventManager](https://github.com/hamster007Github/EventManager) script. This is based on a fork from [mp-eventwatcher](https://github.com/ccev/mp-eventwatcher). 

# Usage
I don't provide a mp file. But you can easily install the plugin by clone this branch into your MAD/plugins/ folder:

- go to MAD/plugins: e.g. `cd /home/<user>/MAD/plugins`
- clone this repo: `git clone https://github.com/hamster007Github/EventManagerViewerPlugin.git`
- go to new folder MAD/plugins/EventManagerViewerPlugin/ and `cp plugin.ini.example plugin.ini`
- adapt `eventcache_path` in plugin.ini to match your setup. Examples:
    example EventManager running in user folder: eventcache_path = /home/user/EventManager/
    example docker setup: eventcache_path = /usr/src/app/plugins/EventManagerViewerPlugin/
    Hint: if you are using MAD docker -> set `eventcache_path` to docker internal plugin folder + set `custome_ventcache_path` in EventManager to MAD docker volume plugin path of this plugin.
- Restart MAD

# Troubleshooting
If you get `Can't load data from .eventcache file` on Event-list page, please check following points:
- EventManager is running?
- .eventcache file is located as defined in `eventcache_path` parameter of your plugin.ini file?
- Using MAD as docker? check hint regarding `eventcache_path` in Usage chapter.
- MAD is executed with same user as EventManager? Otherwise this plugin will not have access to .eventcache file.

