# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from __future__ import annotations
import subprocess
import xbmc
import xbmcgui


class WidevineHelper():
    def __init__(self):
        """
        コンストラクタ
        """

    @ staticmethod
    def transplant_libwidevine():
        # type: () -> None
        """
        パッケージのインストール
        """
        libwidevine_path = xbmc.translatePath('special://home/cdm/libwidevinecdm.so')
        cmd = ['wget', '--no-check-certificate', 'https://pi.vpetkov.net/libwidevinecdm.so', '-o', libwidevine_path]
        progress_bar_title = 'Transplant LibWidevine'
        succeed_message = 'Widevineライブラリを移植しました。'
        failed_message = 'Widevineライブラリの移植に失敗しました。'
        WidevineHelper.__exec_with_dialog(cmd, progress_bar_title, succeed_message, failed_message)

    @ staticmethod
    def __exec_with_dialog(cmd, progress_bar_title, succeed_message, failed_message):
        # type: (str, str, str, str) -> None
        """
        コマンド実行
        """
        exception = None
        progress_bar = xbmcgui.DialogProgress()
        progress_bar.create(progress_bar_title, 'starting...')
        try:
            WidevineHelper.__exec(cmd, lambda progress, message: [
                progress_bar.update(progress, message),
                progress_bar.iscanceled()
            ][-1])
        except subprocess.CalledProcessError as e:
            exception = e
        finally:
            progress_bar.close()
        dialog = xbmcgui.Dialog()
        title = progress_bar_title
        if exception is None:
            message = succeed_message
            dialog.notification(title, message, xbmcgui.NOTIFICATION_INFO, 5000)
        else:
            message = failed_message + '\nReturnCode: ' + unicode(exception.returncode) + '\n' + exception.output
            dialog.ok(title, message)

    @ staticmethod
    def __exec(cmd, update_cb=None):
        # type: (list[str], object) -> None
        """
        コマンド実行
        """
        iscanceled = False
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lastDisplayLine = None
        while True:
            line = proc.stdout.readline()
            if line:
                # 表示テキストがあるなら
                lastDisplayLine = line
                if update_cb is not None:
                    progress = 0
                    if update_cb(progress, line):
                        # キャンセル要望なら
                        if not iscanceled:
                            # まだキャンセルが発行されていないなら
                            proc.terminate()
                            iscanceled = True
            elif proc.poll() is not None:
                # 終了しているなら
                if proc.returncode != 0:
                    cmd_str = ' '.join(['\''+i+'\'' for i in cmd])
                    raise subprocess.CalledProcessError(proc.returncode, cmd_str, output=lastDisplayLine)
                break
