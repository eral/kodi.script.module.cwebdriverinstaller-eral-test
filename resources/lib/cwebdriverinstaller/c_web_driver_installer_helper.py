# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from __future__ import annotations
import subprocess
import xbmc
import xbmcgui
from .c_web_driver_installer import CWebDriverInstaller
from .browser_not_installed_error import BrowserNotInstalledError


class CWebDriverInstallerHelper():
    def __init__(self):
        """
        コンストラクタ
        """

    @ staticmethod
    def append_import_path():
        # type: () -> bool
        """
        WebDriverをインポート出来る様に検索パスを追加する
        ブラウザ・WebDriverの準備が整っていない場合は準備を行う

        Returns
        -------
        result : bool
            True:追加成功, False:失敗(未インストール)
        """
        if not CWebDriverInstaller.is_installed():
            CWebDriverInstallerHelper.install_or_upgrade()
        return CWebDriverInstaller.append_import_path()

    @ staticmethod
    def install_or_upgrade():
        # type: () -> None
        """
        WebDriverのインストール(orアップグレード)
        """
        exception = None
        progress_bar = xbmcgui.DialogProgress()
        progress_bar.create('Install WebDriver', 'starting...')
        try:
            CWebDriverInstaller.install_or_upgrade(lambda progress, message: [
                progress_bar.update(progress, message),
                progress_bar.iscanceled()
            ][-1])
        except BrowserNotInstalledError as e:
            exception = e
        except subprocess.CalledProcessError as e:
            exception = e
        finally:
            progress_bar.close()
        dialog = xbmcgui.Dialog()
        title = 'Install WebDriver'
        if exception is None:
            message = 'WebDriverをインストールしました。'
            dialog.notification(title, message, xbmcgui.NOTIFICATION_INFO, 5000)
        elif isinstance(exception, BrowserNotInstalledError):
            message = 'WebDriverのインストールに失敗しました。\nブラウザの準備が出来ていません。\nブラウザの準備を行いますか？。\n' \
                + 'ReturnCode: ' + unicode(exception.returncode) + '\n' + exception.output
            if dialog.yesno(title, message, yeslabel="Go to the browser", nolabel="No"):
                xbmc.executebuiltin('RunAddon(' + CWebDriverInstaller.chrome_browser_addon_id() + ')')
        else:
            message = 'ReturnCode: ' + unicode(exception.returncode) + '\n' + exception.output
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

    @ staticmethod
    def status():
        # type: () -> None
        """
        インストール状態の表示
        """
        dialog = xbmcgui.Dialog()
        title = 'Install WebDriver Status'
        message = 'Selenium: '
        if CWebDriverInstaller.is_installed():
            message += 'Ready'
        else:
            message += 'Not ready'
        message += '\n'
        message += 'Driver  : '
        if CWebDriverInstaller.is_chrome_driver_installed():
            message += 'Ready'
        else:
            message += 'Not ready'
        message += '\n'
        message += 'Browser : '
        if CWebDriverInstaller.is_chrome_browser_installed():
            message += 'Ready'
        else:
            message += 'Not ready'
        dialog.ok(title, message)
