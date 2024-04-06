from resources.lib.globals import *

class EPG:
    def __init__(self):
        self.monitor = xbmc.Monitor()

    def get_epg_data(self):
        from collections import defaultdict
        epg = defaultdict(list)
            
        start_time = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=24)
        start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        url = f"{BASE_API}/epg?startTime={start_time}&endTime={end_time}&enrichments=follow"        
        xbmc.log(url)
        data = requests.get(url, headers=headers).json()        
        for channel in data['response']:              
            channel_id = channel['data']['channel']['id']
            for program in channel['data']['programsWithAssets']:
                epg_dict = {}
                genres = ''
                
                start_time = program['assets'][0]['accessRights']['startTime'].replace('Z', '')
                stop_time = program['assets'][0]['accessRights']['endTime'].replace('Z', '')
                epg_dict['start'] = start_time
                epg_dict['stop'] = stop_time
                # except:
                #     pass

                # try:
                #     if 'genres' in program['program']:
                #         for genre in program['program']['genres']:
                #             genres += f"{genre['name']} "
                #     epg_dict['genre'] = genres
                # except:
                #     pass

                try:
                    epg_dict['date'] = program['program']['metadata']['originalAiringDate']
                except:
                    pass

                epg_dict['description'] = program['program']['longDescription'] if 'longDescription' in program['program'] else ''
                epg_dict['image'] = program['program']['horizontalImage']
                epg_dict['title'] = program['program']['heading']                
                epg_dict['subtitle'] = program['program']['subheading'] if 'subheading' in program['program'] else ''
                epg_dict['stream'] =  f"plugin://plugin.video.fubotv/?mode=play&channel_id={channel_id}"
                
                epg[channel_id].append(epg_dict)
            
        return epg
    