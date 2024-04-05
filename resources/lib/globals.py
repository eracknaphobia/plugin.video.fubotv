## GLOBALS ##
import base64, calendar, datetime, hashlib, inputstreamhelper, json, os, random, requests, sys, time, re
import traceback, urllib, xmltodict, string, binascii
from datetime import datetime, timedelta, timezone
import xbmc, xbmcvfs, xbmcplugin, xbmcgui, xbmcaddon

urlLib = urllib.parse
urlParse = urlLib


KODI_VERSION_MAJOR = int(xbmc.getInfoLabel('System.BuildVersion').split('.')[0])
ADDON_NAME = 'Fubo TV'
ADDON_ID = 'plugin.video.fubotv'
ADDON_URL = 'plugin://plugin.video.fubotv/'
SETTINGS = xbmcaddon.Addon(id=ADDON_ID)
SETTINGS_LOC = SETTINGS.getAddonInfo('profile')
ADDON_PATH = SETTINGS.getAddonInfo('path')
ADDON_VERSION = SETTINGS.getAddonInfo('version')
ICON = SETTINGS.getAddonInfo('icon')
FANART = SETTINGS.getAddonInfo('fanart')
LANGUAGE = SETTINGS.getLocalizedString

# Sign In Settings
EMAIL = SETTINGS.getSetting('email')
PASSWORD = SETTINGS.getSetting('password')

# Hidden Settings
ACCESS_TOKEN = SETTINGS.getSetting('access_token')

BASE_API = 'https://api.fubo.tv'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'
VERIFY = True

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

def log(msg, level=xbmc.LOGDEBUG):
    if level == xbmc.LOGERROR: msg += ' ,' + traceback.format_exc()
    xbmc.log("------------------------------------------------")
    xbmc.log(ADDON_ID + '-' + ADDON_VERSION + '- ' + msg, level)
    xbmc.log("------------------------------------------------")

def inputDialog(heading=ADDON_NAME, default='', key=xbmcgui.INPUT_ALPHANUM, opt=0, close=0):
    retval = xbmcgui.Dialog().input(heading, default, key, opt, close)
    if len(retval) > 0: return retval


def okDialog(str1, str2='', str3='', header=ADDON_NAME):
    xbmcgui.Dialog().ok(header, str1, str2, str3)


def yesNoDialog(str1, header=ADDON_NAME, yes='', no='', autoclose=0):
    return xbmcgui.Dialog().yesno(header, str1, no, yes, autoclose)


def yesNoCustomDialog(msg, header=ADDON_NAME, custom='', yes='', no='', autoclose=0):
    return xbmcgui.Dialog().yesnocustom(header, msg, custom, no, yes, autoclose)


def notificationDialog(message, header=ADDON_NAME, sound=False, time=1000, icon=ICON):
    try:
        xbmcgui.Dialog().notification(header, message, icon, time, sound)
    except:
        xbmc.executebuiltin("Notification(%s, %s, %d, %s)" % (header, message, time, icon))


def stringToDate(string, date_format):
    if "." in string:
        string = string[0:string.index(".")]
    try:
        return datetime.strptime(str(string), date_format)
    except TypeError:
        return datetime(*(time.strptime(str(string), date_format)[0:6]))


def sortGroup(str):
    arr = str.split(',')
    arr = sorted(arr)
    return ','.join(arr)


def utcToLocal(utc_dt):
    # get integer timestamp to avoid precision lost
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)


def addDir(name, handleID, url, mode, info=None, art=None, menu=None):
    global CONTENT_TYPE, ADDON_URL
    log('Adding directory %s' % name)
    directory = xbmcgui.ListItem(name)
    directory.setProperty('IsPlayable', 'false')
    if info is None: directory.setInfo(type='Video', infoLabels={'mediatype': 'videos', 'title': name})
    else:
        if 'mediatype' in info: CONTENT_TYPE = '%ss' % info['mediatype']
        directory.setInfo(type='Video', infoLabels=info)
    if art is None: directory.setArt({'thumb': ICON, 'fanart': FANART})
    else: directory.setArt(art)

    if menu is not None:
        directory.addContextMenuItems(menu)

    try:
        name = urlLib.quote_plus(name)
    except:
        name = urlLib.quote_plus(strip(name))
    if url != '':
        url = ('%s?url=%s&mode=%s&name=%s' % (ADDON_URL, urlLib.quote_plus(url), mode, name))
    else:
        url = ('%s?mode=%s&name=%s' % (ADDON_URL, mode, name))
    log('Directory %s URL: %s' % (name, url))
    xbmcplugin.addDirectoryItem(handle=handleID, url=url, listitem=directory, isFolder=True)
    xbmcplugin.addSortMethod(handle=handleID, sortMethod=xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)


def addOption(name, handleID, url, mode, info=None, art=None, menu=None):
    global CONTENT_TYPE, ADDON_URL
    log('Adding directory %s' % name)
    directory = xbmcgui.ListItem(name)
    directory.setProperty('IsPlayable', 'false')
    if info is None: directory.setInfo(type='Video', infoLabels={'mediatype': 'videos', 'title': name})
    else:
        if 'mediatype' in info: CONTENT_TYPE = '%ss' % info['mediatype']
        directory.setInfo(type='Video', infoLabels=info)
    if art is None: directory.setArt({'thumb': ICON, 'fanart': FANART})
    else: directory.setArt(art)

    if menu is not None:
        directory.addContextMenuItems(menu)

    try:
        name = urlLib.quote_plus(name)
    except:
        name = urlLib.quote_plus(strip(name))
    if url != '':
        url = ('%s?url=%s&mode=%s&name=%s' % (ADDON_URL, urlLib.quote_plus(url), mode, name))
    else:
        url = ('%s?mode=%s&name=%s' % (ADDON_URL, mode, name))
    log('Directory %s URL: %s' % (name, url))
    xbmcplugin.addDirectoryItem(handle=handleID, url=url, listitem=directory, isFolder=False)
    xbmcplugin.addSortMethod(handle=handleID, sortMethod=xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)


def addLink(name, handleID,  url, mode, info=None, art=None, total=0, channel_id=None, properties=None):
    global CONTENT_TYPE, ADDON_URL
    log('Adding link %s' % name)
    link = xbmcgui.ListItem(name)
    if mode == 'info': link.setProperty('IsPlayable', 'false')
    else: link.setProperty('IsPlayable', 'true')
    # if info is None: link.setInfo(type='Video', infoLabels={'mediatype': 'video', 'title': name})
    # else:
    #     if 'mediatype' in info: CONTENT_TYPE = '%ss' % info['mediatype']
    #     link.setInfo(type='Video', infoLabels=info)
    if art is None: link.setArt({'thumb': ICON, 'fanart': FANART})
    else: link.setArt(art)    
    if properties is not None:
        log('Adding Properties: %s' % str(properties))
        for key, value in properties.items():
            link.setProperty(key, str(value))
    try:
        name = urlLib.quote_plus(name)
    except:
        name = urlLib.quote_plus(strip(name))
    if url != '':
        url = ('%s?url=%s&mode=%s&name=%s&channel_id=%s' % (
            ADDON_URL, urlLib.quote_plus(url), mode, name, channel_id))
    else:
        url = ('%s?mode=%s&name=%s&channel_id=%s' % (ADDON_URL, mode, name, channel_id))
    xbmcplugin.addDirectoryItem(handle=handleID, url=url, listitem=link, totalItems=total)
    xbmcplugin.addSortMethod(handle=handleID, sortMethod=xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
