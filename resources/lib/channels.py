from resources.lib.globals import *


class CHANNELS:
    cms_url = ''
    channels_url = ''
    channels = []
    headers = {
        'User-Agent': USER_AGENT,
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Ad-Id': '4_mACdZaSeS0GJ0d-v',
        'X-Device-Group': 'desktop',
        'X-Device-Type': 'desktop',
        'X-Device-App': 'web',
        'X-Device-Id': 'lcIv8gKevhMscHMB8h',
        'X-Device-Platform': 'desktop',
        'X-Device-Model': 'Windows NT 10.0 Firefox 124.0',
        'X-Client-Version': 'R20240328.1',
        'X-Player-Version': '3.0.2',
        'X-Application-Id': 'fubo',
        'X-Os': 'Windows',
        'X-Os-Version': 'NT 10.0',
        'X-Browser': 'Firefox',
        'X-Browser-Version': '124.0',
        'X-Browser-Engine': 'Gecko',
        'X-Browser-Engine-Version': '20100101',
        'X-Supported-Streaming-Protocols': 'hls,dash',
        'X-Supported-Codecs-List': 'avc',
        'X-DRM-Scheme': 'widevine',
        'X-Supported-Features': 'vidai_my_stuff_moments',
        'X-Preferred-Language': 'en-US',
        'Content-Type': 'application/json',
        'Origin': 'https://www.fubo.tv',
        'Referer': 'https://www.fubo.tv/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site'
    }

    def __init__(self):
        self.get_channels()
       

    def get_channels(self):
        start_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        end_time = datetime.strftime(datetime.now(timezone.utc) + timedelta(hours=1), "%Y-%m-%dT%H:%M:%S.%fZ")
        url = f"https://api.fubo.tv/epg?startTime={start_time}&endTime={end_time}&enrichments=follow"        
        xbmc.log(url)        
        data = requests.get(url, headers=self.headers).json()
        xbmc.log(f"{data}")
        for channel in data['response']:  
            channel_dict = {
                'name': channel['data']['channel']['name'],
                'stream': f"plugin://plugin.video.fubotv/?mode=play&channel_id={channel['data']['channel']['id']}",
                'id': channel['data']['channel']['name'],
                'logo': channel['data']['channel']['logoOnDarkUrl'] ,
                'preset': channel['data']['channel']['id']
            }
            xbmc.log(f"{channel_dict}")
            self.channels.append(channel_dict)         

        return self.channels