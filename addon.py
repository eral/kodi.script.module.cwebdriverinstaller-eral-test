#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import xbmcaddon
import resources.lib.cwebdriverinstaller as cwebdriverinstaller

if __name__ == '__main__':
    if (1 < len(sys.argv)) and (sys.argv[1] == 'install_or_upgrade_web_driver'):
        cwebdriverinstaller.CWebDriverInstallerHelper.install_or_upgrade()
    elif (1 < len(sys.argv)) and (sys.argv[1] == 'uninstall_web_driver'):
        cwebdriverinstaller.CWebDriverInstallerHelper.uninstall()

    elif (1 < len(sys.argv)) and (sys.argv[1] == 'install_apt_chromium'):
        sudoapt = xbmcaddon.Addon().getSettingBool('sudoapt')
        cwebdriverinstaller.AptHelper.install('chromium', sudoapt)
    elif (1 < len(sys.argv)) and (sys.argv[1] == 'uninstall_apt_chromium'):
        sudoapt = xbmcaddon.Addon().getSettingBool('sudoapt')
        cwebdriverinstaller.AptHelper.uninstall('chromium', sudoapt)
    elif (1 < len(sys.argv)) and (sys.argv[1] == 'install_apt_chromedriver'):
        sudoapt = xbmcaddon.Addon().getSettingBool('sudoapt')
        cwebdriverinstaller.AptHelper.install('chromedriver', sudoapt)
    elif (1 < len(sys.argv)) and (sys.argv[1] == 'uninstall_apt_chromedriver'):
        sudoapt = xbmcaddon.Addon().getSettingBool('sudoapt')
        cwebdriverinstaller.AptHelper.uninstall('chromedriver', sudoapt)
    elif (1 < len(sys.argv)) and (sys.argv[1] == 'update_apt'):
        sudoapt = xbmcaddon.Addon().getSettingBool('sudoapt')
        cwebdriverinstaller.AptHelper.update(sudoapt)

    else:
        xbmcaddon.Addon().openSettings()
        cwebdriverinstaller.CWebDriverInstallerHelper.status()
