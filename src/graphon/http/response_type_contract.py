from .protocols import HttpResponseProtocol
from .response import HttpResponse


def _assert_http_response(response: HttpResponse) -> HttpResponseProtocol:
    return response
