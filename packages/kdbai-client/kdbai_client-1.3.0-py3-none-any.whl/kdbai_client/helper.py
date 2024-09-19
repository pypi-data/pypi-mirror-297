
from packaging.version import InvalidVersion, Version

from .api import Session as Session_Rest
from .session import SessionPyKx


def Session(  # noqa: N802
        api_key = None,
        *,
        endpoint = 'http://localhost:8082',
        **kwargs
    ):
    """Factory function to create a connection to a KDB.AI endpoint.

    Args:
        api_key (str): API Key to be used for authentication.
        endpoint (str): Server endpoint to connect to.
        **kwargs (dict): Other keyword arguments

    Example:
        Open a session on KDB.AI Cloud with an api key:

        ```python
        session = Session(endpoint='YOUR_INSTANCE_ENDPOINT', api_key='YOUR_API_KEY')
        ```

        Open a session on a custom KDB.AI instance on http://localhost:8082:

        ```python
        session = kdbai.Session(endpoint='http://localhost:8082')
        ```
    """
    rest_session = Session_Rest(api_key=api_key, endpoint=endpoint)

    versions = rest_session.version()
    try:
        if api_key or Version(versions['serverVersion']) <= Version('1.1.0'):
            return rest_session
    except InvalidVersion:
        pass

    return SessionPyKx(api_key=api_key, endpoint=endpoint, **kwargs)
