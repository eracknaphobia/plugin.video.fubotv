from resources.lib.globals import *


class CHANNELS:
    cms_url = ''
    channels_url = ''
    channels = []

    def __init__(self):
        self.build_channels()
       

    def build_channels(self, channels):
        start_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        end_time = datetime.strftime(datetime.now(timezone.utc) + timedelta(hours=1), "%Y-%m-%dT%H:%M:%S.%fZ")
        url = f"https://api.fubo.tv/epg?startTime={start_time}&endTime={end_time}&enrichments=follow"        
        xbmc.log(url)        
        data = requests.get(url, headers=cls.headers).json()
        xbmc.log(f"{data}")
        for channel in data['response']:                        
            name = item['data']['channel']['name']
            id = item['data']['channel']['id']            
            logo = item['data']['channel']['logoOnDarkUrl']   

            channel_dict = {
                'name': channel['data']['channel']['name'],
                'stream': f'plugin://plugin.video.slingtv/?mode=play&url={channel["qvt_url"]}',
                'id': channel['title'],
                'logo': channel['thumbnail']['url'],
                'preset': channel['channel_number']
            }
            self.channels.append(channel_dict)         


            addLink(name, cls.handleID, '', art=logo, mode='play', channel_id=id)
        for channel in channels:
            if 'metadata' in channel:
                if xbmc.Monitor().abortRequested():
                    break
                # Make language a optional setting
                language = channel['metadata']['language'].lower() if 'language' in channel['metadata'] else ''
                linear_channel = channel['metadata']['is_linear_channel'] if 'is_linear_channel' in channel[
                    'metadata'] else False
                sling_free = True if 'genre' in channel['metadata'] and 'Sling Free' in channel['metadata'][
                    'genre'] else False

                if (linear_channel and language == 'english' and not any(d['name'] == channel['metadata']['channel_name'] for d in self.channels)
                        and (sling_free or FREE_ACCOUNT == 'false')):
                    channel_dict = {
                        'name': channel['metadata']['channel_name'],
                        'stream': f'plugin://plugin.video.slingtv/?mode=play&url={channel["qvt_url"]}',
                        'id': channel['title'],
                        'logo': channel['thumbnail']['url'],
                        'preset': channel['channel_number']
                    }
                    self.channels.append(channel_dict)
