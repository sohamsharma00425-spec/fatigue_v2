"""Root conftest: redirect pytest's basetemp away from OneDrive.

OneDrive's sync daemon locks ``%LOCALAPPDATA%\\Temp\\pytest-of-<user>``
causing ``PermissionError: [WinError 5]`` when pytest tries to enumerate
or create its numbered temp directories. Pointing *basetemp* to a local
directory inside the repo avoids the conflict entirely.
"""

import sys


def pytest_configure(config):
    # Only override if the user hasn't already provided --basetemp
    if config.option.basetemp is None and sys.platform == "win32":
        from pathlib import Path

        config.option.basetemp = str(Path(__file__).parent / ".pytest_tmp")
