import sys
import traceback

import ipdb
import rich_click
from rich.console import Console
from rich.traceback import Traceback

import rl.utils.io

_RICH_TRACEBACK = rl.utils.io.getenv("RL_RICH_TRACEBACK", "0") == "1"
_DEBUG = rl.utils.io.getenv("RL_DEBUG", "1") == "1"


def excepthook(type, value, tb):
    if issubclass(type, KeyboardInterrupt):
        sys.__excepthook__(type, value, tb)
        return
    if _RICH_TRACEBACK:
        traceback_console = Console(stderr=True)
        traceback_console.print(
            Traceback.from_exception(type, value, tb),
        )
    else:
        traceback.print_tb(tb)
    if _DEBUG:
        ipdb.post_mortem(tb)


def command(*args, **kwargs):
    def decorator(f):
        sys.excepthook = excepthook
        return rich_click.command(*args, **kwargs)(f)

    return decorator


def __getattr__(name):
    return getattr(rich_click, name)
