# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from __future__ import annotations
import os
import sys
import string
import subprocess
import json
import re
import xbmcaddon


class CWebDriverInstaller():
    def __init__(self):
        """
        コンストラクタ
        """

    @ staticmethod
    def append_import_path():
        # type: () -> bool
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
    def is_web_driver_installed():
        # type: () -> bool
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
    def is_chrome_browser_installed():
        # type: () -> bool
        """
        Chromeブラウザのインストール確認

        Returns
        -------
        result : bool
            True:インストール済み, False:未インストール
        """
        chrome_browser_path = CWebDriverInstaller.chrome_browser_path()
        result = os.path.isfile(chrome_browser_path)
        return result

    @ staticmethod
    def chrome_browser_path():
        # type: () -> str
        """
        Chromeブラウザのパス

        Returns
        -------
        result : str
            Chromeブラウザのパス
        """
        chrome_browser_addon_id = CWebDriverInstaller.chrome_browser_addon_id()
        result = xbmcaddon.Addon(chrome_browser_addon_id).getAddonInfo('path') + '/chrome-bin/chrome'
        return result

    @ staticmethod
    def chrome_browser_addon_id():
        # type: () -> str
        """
        ChromeブラウザアドオンのID

        Returns
        -------
        result : str
            ChromeブラウザアドオンのID
        """
        result = xbmcaddon.Addon('browser.chrome').getAddonInfo('id')
        return result

    @ staticmethod
    def install_or_upgrade(update_cb=None):
        # type: () -> None
        """
        WebDriverのインストール(orアップグレード)

        Parameters
        ----------
        update_cb : function(int, str)
        更新関数(進捗(0-100), 処理中メッセージ)

        Raises:
        -------
        result : CalledProcessError
            インストール処理がリターンコード0以外で終了した
        """
        installer_path = CWebDriverInstaller.__installer_path()
        installer_meta_path = CWebDriverInstaller.__installer_meta_path()
        install_dir_path = CWebDriverInstaller.__install_dir_path()
        chrome_browser_path = CWebDriverInstaller.chrome_browser_path()
        temp_dir_path = CWebDriverInstaller.__temp_dir_path()

        # 進捗表示用マイルストーンの設定
        if update_cb is not None:
            with open(installer_meta_path) as installer_meta_json_file:
                installer_meta = json.load(installer_meta_json_file)
            milestones = [re.compile(milestone)
                          for milestone in installer_meta['milestones']]
            count_of_achieve_milestones = 0
        # 実行権限確認と付与
        result = subprocess.check_output(['ls', '-l', installer_path])
        if result[3] != 'x':
            subprocess.check_call(['chmod', '+x', installer_path])
        # 実行
        iscanceled = False
        arg = [installer_path, install_dir_path, chrome_browser_path, temp_dir_path]
        proc = subprocess.Popen(arg, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lastDisplayLine = None
        while True:
            line = proc.stdout.readline()
            if line:
                # 表示テキストがあるなら
                lastDisplayLine = line
                if update_cb is not None:
                    if milestones[count_of_achieve_milestones
                                  ].search(line) is not None:
                        count_of_achieve_milestones += 1
                    progress = count_of_achieve_milestones * \
                        100 / len(milestones)
                    update_cb(progress, line)
            elif proc.poll() is not None:
                # 終了しているなら
                if proc.returncode != 0:
                    arg_str = string.join(['\''+i+'\'' for i in arg], ' ')
                    raise subprocess.CalledProcessError(
                        proc.returncode, arg_str, output=lastDisplayLine)
                break
            elif iscanceled:
                # キャンセル要望なら
                proc.terminate()
                break

    @ staticmethod
    def uninstall():
        # type: () -> None
        """
        WebDriverのアンインストール

        Raises:
        -------
        result : CalledProcessError
            インストール処理がリターンコード0以外で終了した
        """
        install_dir_path = CWebDriverInstaller.__install_dir_path()

        subprocess.check_output(
            ['rm', '-rf', install_dir_path])

    __ADDON = xbmcaddon.Addon('script.module.cwebdriverinstaller-eral-test')
    # type: str
    """
    自身のアドオン
    """

    @ staticmethod
    def __installer_path():
        # type: () -> str
        """
        インストールスクリプトのパスの取得

        Returns
        -------
        result : str
            インストールスクリプトのパス
        """
        return CWebDriverInstaller.__ADDON.getAddonInfo('path') + '/resources/data/InstallCWebDriver.sh'

    @ staticmethod
    def __installer_meta_path():
        # type: () -> str
        """
        インストール用メタファイルのパスの取得

        Returns
        -------
        result : str
            インストール用メタファイル
        """
        return CWebDriverInstaller.__ADDON.getAddonInfo('path') + '/resources/data/InstallCWebDriver.meta.json'

    @ staticmethod
    def __install_dir_path():
        # type: () -> str
        """
        インストールディレクトリのパスの取得

        Returns
        -------
        result : str
            インストールディレクトリのパス
        """
        return CWebDriverInstaller.__ADDON.getAddonInfo('path') + '/resources/site-packages/'

    @ staticmethod
    def __temp_dir_path():
        # type: () -> str
        """
        作業ディレクトリパスの取得

        Returns
        -------
        result : str
            作業ディレクトリパス
        """
        return CWebDriverInstaller.__ADDON.getAddonInfo('path') + '/temp/'
