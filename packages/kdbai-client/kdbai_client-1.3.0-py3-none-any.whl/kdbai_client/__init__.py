"""KDB.AI Client for Python."""

from importlib.metadata import PackageNotFoundError, version

from .api import _set_version, KDBAIException, MAX_DATETIME, MIN_DATETIME, Table  # noqa
from .api import Session as SessionRest  # noqa
from .constants import VdbScopes  # noqa
from .helper import Session  # noqa
from .session import SessionPyKx  # noqa
from .table import TablePyKx  # noqa


try:
    __version__ = version('kdbai_client')
    if "dev" in __version__ or __version__ == "0.0.0":
        __version__ = 'dev'
except PackageNotFoundError:  # pragma: no cover
    __version__ = 'dev'
_set_version(__version__)


__all__ = sorted(['__version__', 'KDBAIException', 'MIN_DATETIME', 'MAX_DATETIME', 'SessionPyKx', 'TablePyKx',
                  'SessionRest', 'TableRest', 'VdbScopes'])


def __dir__():
    return __all__
