import abc
from collections.abc import Mapping
from typing import Any, Protocol

from .response import HttpResponse


class HttpResponseProtocol(Protocol):
    @property
    @abc.abstractmethod
    def headers(self) -> Mapping[str, str]: ...

    @property
    @abc.abstractmethod
    def content(self) -> bytes: ...

    @property
    @abc.abstractmethod
    def status_code(self) -> int: ...

    @property
    @abc.abstractmethod
    def text(self) -> str: ...

    @property
    @abc.abstractmethod
    def is_success(self) -> bool: ...

    @abc.abstractmethod
    def raise_for_status(self) -> None: ...


class HttpClientProtocol(Protocol):
    @property
    @abc.abstractmethod
    def max_retries_exceeded_error(self) -> type[Exception]: ...

    @property
    @abc.abstractmethod
    def request_error(self) -> type[Exception]: ...

    @abc.abstractmethod
    def get(self, url: str, max_retries: int = ..., **kwargs: Any) -> HttpResponse: ...

    @abc.abstractmethod
    def head(self, url: str, max_retries: int = ..., **kwargs: Any) -> HttpResponse: ...

    @abc.abstractmethod
    def post(self, url: str, max_retries: int = ..., **kwargs: Any) -> HttpResponse: ...

    @abc.abstractmethod
    def put(self, url: str, max_retries: int = ..., **kwargs: Any) -> HttpResponse: ...

    @abc.abstractmethod
    def delete(
        self,
        url: str,
        max_retries: int = ...,
        **kwargs: Any,
    ) -> HttpResponse: ...

    @abc.abstractmethod
    def patch(
        self,
        url: str,
        max_retries: int = ...,
        **kwargs: Any,
    ) -> HttpResponse: ...
