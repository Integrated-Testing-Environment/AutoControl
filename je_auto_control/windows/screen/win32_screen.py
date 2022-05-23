import sys
from typing import List

from je_auto_control.utils.exception.exception_tag import windows_import_error
from je_auto_control.utils.exception.exceptions import AutoControlException

if sys.platform not in ["win32", "cygwin", "msys"]:
    raise AutoControlException(windows_import_error)

import ctypes

_user32 = ctypes.windll.user32
_user32.SetProcessDPIAware()


def size() -> List[int, int]:
    """
    get screen size
    """
    return [_user32.GetSystemMetrics(0), _user32.GetSystemMetrics(1)]
