from __future__ import annotations
from typing import Callable
import os
import sys
import shlex
import subprocess
import json
import re
import xbmcaddon
from .browser_not_installed_error import BrowserNotInstalledError


class CWebDriverInstaller():
    def __init__(self):
        """
        コンストラクタ
        """

    @ staticmethod
    def append_import_path() -> bool:
        """
        WebDriverをインポート出来る様に検索パスを追加する

        Returns
        -------
        result : bool
            True:追加成功, False:失敗(未インストール)
        """
        if not CWebDriverInstaller.is_web_driver_installed():
            return False
        install_dir_path = CWebDriverInstaller.__install_dir_path()
        sys.path.append(install_dir_path)
        return True

    @ staticmethod
    def is_web_driver_installed() -> bool:
        """
        WebDriverのインストール確認

        Returns
        -------
        result : bool
            True:インストール済み, False:未インストール
        """
        install_dir_path = CWebDriverInstaller.__install_dir_path()
        result = os.path.isdir(install_dir_path)
        return result

    @ staticmethod
    def is_chrome_browser_installed() -> bool:
        """
        Chromeブラウザのインストール確認

        Returns
        -------
        result : bool
            True:インストール済み, False:未インストール
        """
        result = False
        chrome_browser_path = CWebDriverInstaller.chrome_browser_path()
        if chrome_browser_path is not None:
            result = os.path.isfile(chrome_browser_path)
        return result

    @ staticmethod
    def chrome_browser_path() -> str:
        """
        Chromeブラウザのパス

        Returns
        -------
        result : str
            Chromeブラウザのパス
        """
        result = None
        if result is None:
            # ブラウザアドオンを検索
            try:
                chrome_browser_addon_id = 'browser.chrome'
                chrome_browser_addon = xbmcaddon.Addon(chrome_browser_addon_id)
                result = chrome_browser_addon.getAddonInfo('path') + 'chrome-bin/chrome'
            except RuntimeError as e:
                if str(e).startswith('Unknown addon id'):
                    pass
                else:
                    raise
        if result is None:
            exec_file_names = ['google-chrome', 'chromium', 'chrome']
            if result is None:
                # whichで検索
                for exec_file_name in exec_file_names:
                    which_result = subprocess.run(['which', exec_file_name], capture_output=True)
                    if which_result.returncode == 0:
                        result = which_result.stdout.decode().rstrip()
                        break
            if result is None:
                # 決め打ち検索
                for exec_file_name in exec_file_names:
                    exec_file_path = '/usr/bin/' + exec_file_name
                    if os.path.isfile(exec_file_path):
                        result = exec_file_path
                        break
        return result

    @ staticmethod
    def install_or_upgrade(update_cb: Callable[[int, str], bool] = None) -> None:
        """
        WebDriverのインストール(orアップグレード)

        Parameters
        ----------
        update_cb : Callable[[int, str], bool]
        更新関数(進捗(0-100), 処理中メッセージ)

        Raises:
        -------
        result : CalledProcessError
            インストール処理がリターンコード0以外で終了した
        """
        installer_path = CWebDriverInstaller.__installer_path()
        installer_meta_path = CWebDriverInstaller.__installer_meta_path()
        install_dir_path = CWebDriverInstaller.__install_dir_path()
        temp_dir_path = CWebDriverInstaller.__temp_dir_path()

        # 進捗表示用マイルストーンの設定
        if update_cb is not None:
            with open(installer_meta_path) as installer_meta_json_file:
                installer_meta = json.load(installer_meta_json_file)
            milestones = [re.compile(milestone) for milestone in installer_meta['milestones']]
            count_of_achieve_milestones = 0
        # 実行権限確認と付与
        result = subprocess.check_output(['ls', '-l', installer_path])
        if result[3] != 'x':
            subprocess.check_call(['chmod', '+x', installer_path])
        # 実行
        iscanceled = False
        arg = [installer_path, install_dir_path, temp_dir_path]
        proc = subprocess.Popen(arg, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lastDisplayLine = None
        while True:
            line = proc.stdout.readline()
            if line:
                # 表示テキストがあるなら
                line = line.decode().rstrip()
                print('line: ' + line)
                lastDisplayLine = line
                if update_cb is not None:
                    if milestones[count_of_achieve_milestones].search(line) is not None:
                        count_of_achieve_milestones += 1
                    progress = count_of_achieve_milestones * 100 // len(milestones)
                    if update_cb(progress, line):
                        # キャンセル要望なら
                        if not iscanceled:
                            # まだキャンセルが発行されていないなら
                            proc.terminate()
                            iscanceled = True
            elif proc.poll() is not None:
                # 終了しているなら
                if proc.returncode == CWebDriverInstaller.__BROWSER_NOT_INSTALLED_RETURN_CODE:
                    arg_str = shlex.join(arg)
                    raise BrowserNotInstalledError(proc.returncode, arg_str, output=lastDisplayLine)
                elif proc.returncode != 0:
                    arg_str = shlex.join(arg)
                    raise subprocess.CalledProcessError(proc.returncode, arg_str, output=lastDisplayLine)
                break

    @ staticmethod
    def uninstall() -> None:
        """
        WebDriverのアンインストール

        Raises:
        -------
        result : CalledProcessError
            インストール処理がリターンコード0以外で終了した
        """
        install_dir_path = CWebDriverInstaller.__install_dir_path()

        subprocess.check_output(['rm', '-rf', install_dir_path])

    __ADDON: str = xbmcaddon.Addon('script.module.cwebdriverinstaller-eral-test')
    """
    自身のアドオン
    """

    __BROWSER_NOT_INSTALLED_RETURN_CODE: int = 101
    """
    ブラウザ未インストールエラーのリターンコード
    """

    @ staticmethod
    def __installer_path() -> str:
        """
        インストールスクリプトのパスの取得

        Returns
        -------
        result : str
            インストールスクリプトのパス
        """
        return CWebDriverInstaller.__ADDON.getAddonInfo('path') + 'resources/data/InstallCWebDriver.sh'

    @ staticmethod
    def __installer_meta_path() -> str:
        """
        インストール用メタファイルのパスの取得

        Returns
        -------
        result : str
            インストール用メタファイル
        """
        return CWebDriverInstaller.__ADDON.getAddonInfo('path') + 'resources/data/InstallCWebDriver.meta.json'

    @ staticmethod
    def __install_dir_path() -> str:
        """
        インストールディレクトリのパスの取得

        Returns
        -------
        result : str
            インストールディレクトリのパス
        """
        return CWebDriverInstaller.__ADDON.getAddonInfo('path') + 'resources/site-packages/'

    @ staticmethod
    def __temp_dir_path() -> str:
        """
        作業ディレクトリパスの取得

        Returns
        -------
        result : str
            作業ディレクトリパス
        """
        return CWebDriverInstaller.__ADDON.getAddonInfo('path') + 'temp/'
