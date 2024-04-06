from resources.lib.globals import *


class CHANNELS:
    cms_url = ''
    channels_url = ''
    channels = []

    def __init__(self):
        self.get_channels()
       

    def get_channels(self):
        start_time = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)
        start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        
        url = f"{BASE_API}/epg?startTime={start_time}&endTime={end_time}&enrichments=follow"        
        xbmc.log(url)        
        data = requests.get(url, headers=headers).json()        
        for channel in data['response']:  
            channel_dict = {
                'name': channel['data']['channel']['name'],
                'stream': f"plugin://plugin.video.fubotv/?mode=play&channel_id={channel['data']['channel']['id']}",
                'id': channel['data']['channel']['id'],
                'logo': channel['data']['channel']['logoOnDarkUrl']
                #'preset': channel['data']['channel']['id']
            }
            xbmc.log(f"{channel_dict}")
            self.channels.append(channel_dict)         

        return self.channels