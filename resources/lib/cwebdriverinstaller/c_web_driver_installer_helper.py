# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from __future__ import annotations
import xbmcgui
from .c_web_driver_installer import CWebDriverInstaller


class CWebDriverInstallerHelper():
    def __init__(self):
        """
        コンストラクタ
        """

    @ staticmethod
    def install_or_upgrade():
        # type: () -> None
        """
        WebDriverのインストール(orアップグレード)
        """
        returncode = 0
        returnmessage = None
        progress_bar = xbmcgui.DialogProgress()
        progress_bar.create('Install WebDriver', 'starting...')
        try:
            CWebDriverInstaller.install_or_upgrade(lambda progress, message: [
                progress_bar.update(progress, message),
                progress_bar.iscanceled()
            ][-1])
        except subprocess.CalledProcessError as e:
            returncode = e.returncode
            returnmessage = e.output
        finally:
            progress_bar.close()
        dialog = xbmcgui.Dialog()
        title = 'Install WebDriver'
        if returnmessage is None:
            message = 'WebDriverをインストールしました。'
            dialog.notification(title, message, xbmcgui.NOTIFICATION_INFO, 5000)
        else:
            message = 'ReturnCode: ' + unicode(returncode) + '\n\n' + returnmessage
            dialog.ok(title, message)

    @ staticmethod
    def uninstall():
        # type: () -> None
        """
        WebDriverのアンインストール
        """
        returncode = 0
        returnmessage = None
        try:
            CWebDriverInstaller.uninstall()
        except subprocess.CalledProcessError as e:
            returncode = e.returncode
            returnmessage = e.output
        dialog = xbmcgui.Dialog()
        title = 'Uninstall WebDriver'
        if returnmessage is None:
            message = 'WebDriverをアンインストールしました。'
            dialog.notification(title, message, xbmcgui.NOTIFICATION_INFO, 5000)
        else:
            message = 'ReturnCode: ' + unicode(returncode) + '\n\n' + returnmessage
            dialog.ok(title, message)
