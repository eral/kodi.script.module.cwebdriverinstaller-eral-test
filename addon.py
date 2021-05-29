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
    elif (1 < len(sys.argv)) and (sys.argv[1] == 'install_apt_chromiumdriver'):
        sudoapt = xbmcaddon.Addon().getSettingBool('sudoapt')
        cwebdriverinstaller.AptHelper.install('chromium-driver', sudoapt)
    elif (1 < len(sys.argv)) and (sys.argv[1] == 'uninstall_apt_chromiumdriver'):
        sudoapt = xbmcaddon.Addon().getSettingBool('sudoapt')
        cwebdriverinstaller.AptHelper.uninstall('chromium-driver', sudoapt)
    elif (1 < len(sys.argv)) and (sys.argv[1] == 'update_apt'):
        sudoapt = xbmcaddon.Addon().getSettingBool('sudoapt')
        cwebdriverinstaller.AptHelper.update(sudoapt)

    elif (1 < len(sys.argv)) and (sys.argv[1] == 'transplant_libwidevine_from_chromium_me'):
        cwebdriverinstaller.WidevineHelper.transplant_libwidevine()

    else:
        xbmcaddon.Addon().openSettings()
        cwebdriverinstaller.CWebDriverInstallerHelper.status()
