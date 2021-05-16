#!/usr/bin/env python3

from __future__ import annotations

import sys
import xbmcaddon
from resources.lib.cwebdriverinstaller import CWebDriverInstallerHelper

if __name__ == '__main__':
    if (1 < len(sys.argv)) and (sys.argv[1] == 'install_or_upgrade_web_driver'):
        CWebDriverInstallerHelper.install_or_upgrade()
    elif (1 < len(sys.argv)) and (sys.argv[1] == 'uninstall_web_driver'):
        CWebDriverInstallerHelper.uninstall()
    else:
        xbmcaddon.Addon().openSettings()
        CWebDriverInstallerHelper.status()
