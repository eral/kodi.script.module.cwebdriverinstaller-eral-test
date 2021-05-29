# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from __future__ import annotations
import subprocess
import xbmcgui


class AptHelper():
    def __init__(self):
        """
        コンストラクタ
        """

    @ staticmethod
    def update(is_sudo):
        # type: (bool) -> None
        """
        パッケージのインストール
        """
        cmd = ['apt-get', '-y', 'update']
        if is_sudo:
            cmd = ['sudo'] + cmd
        progress_bar_title = 'Update apt'
        succeed_message = 'aptをアップデートしました。'
        failed_message = 'aptのアップデートに失敗しました。'
        AptHelper.__exec_with_dialog(cmd, progress_bar_title, succeed_message, failed_message)

    @ staticmethod
    def install(package_name, is_sudo):
        # type: (str, bool) -> None
        """
        パッケージのインストール
        """
        cmd = ['apt-get', '-y', 'install', '--no-install-recommends', package_name]
        if is_sudo:
            cmd = ['sudo'] + cmd
        progress_bar_title = 'Install ' + package_name
        succeed_message = package_name + 'をインストールしました。'
        failed_message = package_name + 'のインストールに失敗しました。'
        AptHelper.__exec_with_dialog(cmd, progress_bar_title, succeed_message, failed_message)

    @ staticmethod
    def uninstall(package_name, is_sudo):
        # type: (str, bool) -> None
        """
        パッケージのアンインストール
        """
        cmd = ['apt-get', '-y', 'remove', '--purge', package_name]
        if is_sudo:
            cmd = ['sudo'] + cmd
        progress_bar_title = 'Uninstall ' + package_name
        succeed_message = package_name + 'をアンインストールしました。'
        failed_message = package_name + 'のアンインストールに失敗しました。'
        AptHelper.__exec_with_dialog(cmd, progress_bar_title, succeed_message, failed_message)

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
            AptHelper.__exec(cmd, lambda progress, message: [
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
