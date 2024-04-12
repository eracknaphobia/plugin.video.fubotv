from resources.lib.globals import *

class Fubotv:

    # default_headers = {
    #     "accept":"*/*",
    #     "accept-encoding":"gzip, deflate, br",
    #     "accept-language":"en-US,en;q=0.5",
    #     "origin":"https://www.fubo.tv",
    #     "referer":"https://www.fubo.tv/",
    #     "user-agent": USER_AGENT
    # }

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

    @classmethod
    def __init__(cls, sysARG):
        cls.sysARG = sysARG
        cls.handleID = int(cls.sysARG[1])
        cls.mode = None
        cls.channel_id = None
        cls.get_params()

    @classmethod
    def run(cls):
        
        if cls.mode is None:            
            cls.build_menu()
        elif cls.mode == "channels":
            cls.ch_list()
        elif cls.mode == "play":
            cls.check_login()
            cls.play()
        elif cls.mode == "settings":
            xbmcaddon.Addon().openSettings()
        elif cls.mode == "logout":
            cls.logout()

        xbmcplugin.setContent(cls.handleID, "Episodes")
        xbmcplugin.addSortMethod(cls.handleID, xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.addSortMethod(cls.handleID, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.addSortMethod(cls.handleID, xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.addSortMethod(cls.handleID, xbmcplugin.SORT_METHOD_TITLE)
        xbmcplugin.endOfDirectory(cls.handleID, updateListing=False, cacheToDisc=False)

        xbmc.executebuiltin('Container.SetSortMethod(1)')

    @classmethod
    def get_params(cls):
        log('Retrieving parameters')

        cls.params = dict(urlParse.parse_qsl(cls.sysARG[2][1:]))       
        try: cls.url = urlLib.unquote(cls.params['url'])
        except: pass
        try: cls.name = urlLib.unquote_plus(cls.params['name'])
        except: pass
        try: cls.mode = cls.params['mode']
        except: pass
        try: cls.channel_id = cls.params['channel_id']
        except: pass

    @classmethod
    def build_menu(cls):
        log('Building Menu')

        # if cls.mode is None:
        addDir("Channels", cls.handleID, '', mode='channels')
        addOption("Settings", cls.handleID, '', mode='settings')

    @classmethod
    def check_login(cls, email=EMAIL, password=PASSWORD):
        # First launch, credentials empty
        if email == '' or password == '':            
            answer = yesNoDialog(LANGUAGE(30006), no=LANGUAGE(30004), yes=LANGUAGE(30005))
            if answer == 1:
                global EMAIL, PASSWORD
                email = inputDialog(LANGUAGE(30002))
                password = inputDialog(LANGUAGE(30003), opt=xbmcgui.ALPHANUM_HIDE_INPUT)
                SETTINGS.setSetting('email', email)
                SETTINGS.setSetting('password', password)
                EMAIL = email
                PASSWORD = password 
                cls.login()
                notificationDialog("Logged In Successfully", header=ADDON_NAME, sound=False, time=1000, icon=ICON)
            else:
                sys.exit()                           
        else:
            token_expires = SETTINGS.getSetting('token_expires')
            if token_expires is None or token_expires == '':
                cls.login()
            elif stringToDate(token_expires, "%Y-%m-%d %H:%M:%S") < datetime.now():
                cls.login()

    @classmethod
    def login(cls):        
        payload = {
            "email": EMAIL,
            "password": PASSWORD
        }

        r = requests.put(f"{BASE_API}/signin", headers=cls.headers, json=payload)
        xbmc.log(f"{payload} {r.text}")
        if r.ok and 'access_token' in r.json():
            global ACCESS_TOKEN
            SETTINGS.setSetting('access_token', r.json()['access_token'])
            SETTINGS.setSetting('id_token', r.json()['id_token'])
            SETTINGS.setSetting('refresh_token', r.json()['refresh_token'])
            SETTINGS.setSetting('token_expires', datetime.strftime(datetime.now() + timedelta(hours=1), "%Y-%m-%d %H:%M:%S"))            
            ACCESS_TOKEN = SETTINGS.getSetting('access_token')
        else:
            message = r.json()['error']['message']
            notificationDialog(message, header=ADDON_NAME, sound=False, time=1000, icon=ICON)
            sys.exit()

    @classmethod
    def logout(cls):                
        SETTINGS.setSetting('email', '')
        SETTINGS.setSetting('password', '')
        SETTINGS.setSetting('access_token', '')
        SETTINGS.setSetting('id_token', '')
        SETTINGS.setSetting('refresh_token', '')
        SETTINGS.setSetting('token_expires', '')

    @classmethod
    def ch_list(cls):        
        start_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        end_time = datetime.strftime(datetime.now(timezone.utc) + timedelta(hours=1), "%Y-%m-%dT%H:%M:%S.%fZ")
        url = f"https://api.fubo.tv/epg?startTime={start_time}&endTime={end_time}&enrichments=follow"        
        xbmc.log(url)        
        data = requests.get(url, headers=cls.headers).json()
        xbmc.log(f"{data}")
        for item in data['response']:                        
            name = item['data']['channel']['name']
            id = item['data']['channel']['id']            
            logo = item['data']['channel']['logoOnDarkUrl']            

            addLink(name, cls.handleID, '', art=logo, mode='play', channel_id=id)
        
    
    @classmethod
    def get_stream_url(cls, ch_id):
        stream_url = ''
        drm = {}
        cls.headers["authorization"] = f"Bearer {ACCESS_TOKEN}"
        cls.headers["X-DRM-Scheme"] = "widevine"
        cls.headers["X-Supported-Streaming-Protocols"] = "dash"
        
        url = f"https://api.fubo.tv/vapi/asset/v1?channelId={ch_id}&trkOp=guide-schedule&trkOriginAppSection=guide&trkOriginPage=guide&type=live"
        xbmc.log(url)
        r = requests.get(url, headers=cls.headers)  
        log(f"{r.text}")          
        if r.ok:            
            if 'stream' in r.json():
                stream_url= r.json()['stream']['url']
            elif 'streamUrls' in r.json():
                stream_url= r.json()['streamUrls'][0]['url']
            if 'drm' in r.json():
                drm = r.json()['drm']
        else:
            message = r.json()['error']['message']
            notificationDialog(message, header=ADDON_NAME, sound=False, time=1000, icon=ICON)
            sys.exit()
        
        return stream_url, drm
    
    @classmethod
    def play(cls):        
        xbmc.log(cls.channel_id)        
        stream_url, drm = cls.get_stream_url(cls.channel_id)       
        xbmc.log(stream_url)

        listitem = xbmcgui.ListItem(path=stream_url)        
        listitem.setProperty('inputstream', 'inputstream.adaptive')
        listitem.setProperty("inputstream.adaptive.manifest_headers",  f"User-Agent={USER_AGENT}")
        listitem.setProperty('inputstream.adaptive.stream_headers', f"User-Agent={USER_AGENT}")
        if '.m3u8' in stream_url:
            listitem.setProperty("inputstream.adaptive.manifest_type", "hls")  
        elif '.mpd' in stream_url:
            listitem.setProperty("inputstream.adaptive.manifest_type", "mpd")  
            listitem.setMimeType('application/xml+dash')       

        # DRM Content
        if 'provider' in drm and drm['provider'] != '':
            is_helper = inputstreamhelper.Helper('mpd', drm='widevine')
            if not is_helper.check_inputstream():
                sys.exit()
            listitem.setContentLookup(False)
            listitem.setProperty('inputstream.adaptive.license_type', 'com.widevine.alpha')
            
            license_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
                'Content-Type': 'application/octet-stream',
                'Origin': 'https://www.fubo.tv',
                'Referer': 'https://www.fubo.tv/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'TE': 'trailers',
                'DNT': '1'
            }

            xbmc.log(f"{drm}")
            from urllib.parse import urlencode
            license_config = { # for Python < v3.7 you should use OrderedDict to keep order
                'license_server_url': f"{drm['licenseUrl']}&ls_session={drm['token']}",
                'headers': urlencode(license_headers),
                'post_data': 'R{SSM}',
                'response_data': 'R'
            }            
            listitem.setProperty('inputstream.adaptive.license_key', '|'.join(license_config.values()))           
        else:                      
            listitem.setProperty("inputstream.adaptive.license_key", f"|User-Agent={USER_AGENT}")
        

        xbmcplugin.setResolvedUrl(cls.handleID, True, listitem)