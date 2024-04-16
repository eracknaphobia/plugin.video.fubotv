# plugin.video.fubotv
![Build Status](https://img.shields.io/badge/Build-Beta-orange)
![License](https://img.shields.io/badge/License-GPL--3.0--only-success.svg)
![Kodi Version](https://img.shields.io/badge/Kodi-Nexus%2B-brightgreen)
![Contributors](https://img.shields.io/badge/Contributors-eracknaphobia-darkgray)

Fubo TV Add-On for Kodi
* Uses [IPTV Manager](https://github.com/add-ons/service.iptv.manager) to integrate live channels into Kodi EPG

![](https://github.com/eracknaphobia/plugin.video.fubotv/blob/master/resources/images/icon.png?raw=true)

## Initial Setup
* Install [IPTV Manager from their github repo](https://github.com/add-ons/service.iptv.manager/releases/) as the version in the official kodi repo doesn't work correctly.
    * Make sure to disable updates for iptv manager or it will install the kodi repo version over top since it is a version ahead currently
* Open the Fubo TV addon it will prompt you to login to your account
* Once you've logged in successfully go to IPTV Manager Settings and select **Refresh channels and guide now**
    * You may have to Reset PVR Settings on the first run (Settings > PVR & Live TV > General > Clear Data > All)
* It's recommended that you set the **Refresh interval** in IPTV Manager to 12 hours (or lower) since guide data is 24 hr period this will prevent any gaps in the guide

## Links

* [Fubo TV](https://www.fubo.tv/)
* [Kodi Forum Thread](https://forum.kodi.tv/showthread.php?tid=376961)
* [Kodi Wiki](https://kodi.wiki/view/Main_Page)
