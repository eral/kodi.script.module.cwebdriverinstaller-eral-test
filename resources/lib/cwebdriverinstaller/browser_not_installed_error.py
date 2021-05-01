# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from __future__ import annotations
import subprocess


class BrowserNotInstalledError(subprocess.CalledProcessError):
    def __init__(self, returncode, cmd, output=None):
        """
        コンストラクタ
        """
        super(BrowserNotInstalledError, self).__init__(returncode, cmd, output)
