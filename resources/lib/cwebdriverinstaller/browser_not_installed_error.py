from __future__ import annotations
from subprocess import CalledProcessError


class BrowserNotInstalledError(CalledProcessError):
    def __init__(self, returncode, cmd, output=None):
        """
        コンストラクタ
        """
        super().__init__(returncode, cmd, output)
