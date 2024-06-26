import os

import httpx


limits: httpx.Limits = httpx.Limits(
    max_keepalive_connections=None,  # Never limit
    max_connections=None  # Never limit
)


def create_httpx_client(error_stacktrace: bool, **kwargs) -> httpx.AsyncClient:
    _io_timeout = float(os.environ.get("CRIADEX_SDK_IO_TIMEOUT", 120.0))
    _connect_timeout = float(os.environ.get("CRIADEX_SDK_CONNECT_TIMEOUT", 10.0))

    timeout: httpx.Timeout = httpx.Timeout(
        read=_io_timeout,
        write=_io_timeout,
        connect=_connect_timeout,
        pool=_connect_timeout  # retrieving free connection
    )

    return httpx.AsyncClient(
        headers={**kwargs.pop("headers", dict()), "x-api-stacktrace": str(error_stacktrace).lower()},
        limits=limits,
        timeout=timeout,
        **kwargs
    )
