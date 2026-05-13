from .client import HttpxHttpClient
from .protocols import HttpClientProtocol


def _assert_httpx_http_client(client: HttpxHttpClient) -> HttpClientProtocol:
    return client
