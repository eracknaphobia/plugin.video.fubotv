from resources.lib.globals import *

class EPG:
    def __init__(self):
        self.monitor = xbmc.Monitor()

    def get_epg_data(self):
        from collections import defaultdict
        epg = defaultdict(list)
            
        start_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        end_time = datetime.strftime(datetime.now(timezone.utc) + timedelta(hours=1), "%Y-%m-%dT%H:%M:%S.%fZ")
        url = f"https://api.fubo.tv/epg?startTime={start_time}&endTime={end_time}&enrichments=follow"        
        xbmc.log(url)        
        data = requests.get(url, headers=headers).json()
        xbmc.log(f"{data}")
        for channel in data['response']:              
            channel_id = channel['data']['channel']['id']
            for program in channel['data']['programsWithAssets']:
                epg_dict = {}
                genres = ''
                
                #xbmc.log(f'{datetime.strptime(program['assets'][0]['accessRights']['startTime'], "%Y-%m-%dT%H:%M:%SZ").astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')}')

                try:
                    start_time = datetime.strptime(program['assets'][0]['accessRights']['startTime'], "%Y-%m-%dT%H:%M:%SZ").astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
                    stop_time = datetime.strptime(program['assets'][0]['accessRights']['endTime'], "%Y-%m-%dT%H:%M:%SZ").astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
                    epg_dict['start'] = start_time
                    epg_dict['stop'] = stop_time
                except:
                    pass

                # try:
                #     if 'genres' in program['program']:
                #         for genre in program['program']['genres']:
                #             genres += f"{genre['name']} "
                #     epg_dict['genre'] = genres
                # except:
                #     pass

                try:
                    epg_dict['date'] = program['program']['metadata']['originalAiringDate']
                    epg_dict['description'] = program['program']['longDescription']
                    epg_dict['image'] = program['program']['featuredImage']
                except:
                    pass
                                            
                epg_dict['title'] = program['program']['heading']                
                epg_dict['subtitle'] = program['program']['title']
                epg_dict['stream'] =  f"plugin://plugin.video.fubotv/?mode=play&channel_id={channel_id}"
                
            
            epg[channel_id].append(epg_dict)

        return epg

        # self.get_channels()

        # session = requests.Session()
        # retry = Retry(connect=3, backoff_factor=0.5)
        # adapter = HTTPAdapter(max_retries=retry)
        # session.mount('http://', adapter)
        # session.mount('https://', adapter)

        # progress = xbmcgui.DialogProgressBG()
        # progress.create("Sling TV", "Getting EPG Info...")
        # for day in range(0, 1):
        #     i = 0
        #     for channel in self.channels:
        #         if self.monitor.abortRequested():
        #             break
        #         url_timestamp = (datetime.date.today() + datetime.timedelta(days=day)).strftime(
        #             "%y%m%d") + datetime.datetime.utcnow().strftime("%H%M")
        #         schedule_url = f"{self.cms_url}/cms/publish3/channel/schedule/24/{url_timestamp}/1/{channel[0]}.json"
        #         xbmc.log(f"{channel[2]}")
        #         xbmc.log(schedule_url)
        #         i += 1
        #         progress.update(int((i / len(self.channels)) * 100), message=f"{channel[2]}")
                
        #         try:
        #             r = session.get(schedule_url, headers=HEADERS, timeout=10)
        #         except:
        #             pass

        #         if not r.ok or 'schedule' not in r.json() or 'scheduleList' not in r.json()['schedule']: continue
        #         channel_id = channel[1]
        #         stream_url = channel[4]
        #         # try:
        #         for slot in r.json()['schedule']['scheduleList']:
        #             epg_dict = {}
        #             start_time = datetime.datetime.utcfromtimestamp(
        #                 int(str(slot['schedule_start']).replace('.000', ''))).strftime('%Y-%m-%dT%H:%M:%S')
        #             stop_time = datetime.datetime.utcfromtimestamp(
        #                 int(str(slot['schedule_stop']).replace('.000', ''))).strftime('%Y-%m-%dT%H:%M:%S')
        #             title = str(slot['title'])
        #             sub_title = slot['metadata']['episode_title'] if 'episode_title' in slot['metadata'] else ''
        #             desc = slot['metadata']['description'] if 'description' in slot['metadata'] else ''
        #             xbmc.log(title)
        #             image = ''
        #             if 'thumbnail' in slot and slot['thumbnail']:
        #                 image = slot['thumbnail']['url']
        #             elif 'program' in slot and slot['program']['franchise_image'] is not None:
        #                 image = slot['program']['franchise_image']
        #             air_date = slot['orig_air_date'] if 'orig_air_date' in slot else ''
        #             genres = ''
        #             if 'genre' in slot['metadata']:
        #                 for genre in slot['metadata']['genre']:
        #                     genres += f"{genre} "

        #             epg_dict['start'] = start_time
        #             epg_dict['stop'] = stop_time
        #             epg_dict['title'] = title
        #             epg_dict['description'] = desc
        #             epg_dict['subtitle'] = sub_title
        #             epg_dict['stream'] = stream_url
        #             epg_dict['image'] = image
        #             epg_dict['date'] = air_date
        #             epg_dict['genre'] = genres

        #             if 'episode_season' in slot['metadata'] and 'episode_number' in slot['metadata']:
        #                 s = slot['metadata']['episode_season']
        #                 e = slot['metadata']['episode_number']
        #                 if s != 0 and e != 0:
        #                     episode = f'S{s}E{e}'
        #                     epg_dict['episode'] = episode

        #             epg[channel_id].append(epg_dict)

        #     progress.close()
        #     return epg
