import routing
from resources.lib.globals import *
from resources.lib.fubo import Fubotv

plugin = routing.Plugin()

@plugin.route('/iptv/channels')
def iptv_channels():
    """Return JSON-STREAMS formatted data for all live channels"""
    from resources.lib.iptvmanager import IPTVManager
    port = int(plugin.args.get('port')[0])
    IPTVManager(port).send_channels()


@plugin.route('/iptv/epg')
def iptv_epg():
    """Return JSON-EPG formatted data for all live channel EPG data"""
    from resources.lib.iptvmanager import IPTVManager
    port = int(plugin.args.get('port')[0])
    IPTVManager(port).send_epg()


@plugin.route('/')
def default():    
    Fubotv(sys.argv).run()
    
    
if __name__ == '__main__':
    plugin.run()
