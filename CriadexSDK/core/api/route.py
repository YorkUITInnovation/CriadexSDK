import functools
import logging
import os
import traceback
from abc import abstractmethod
from functools import wraps
from typing import Optional, Callable, Any, Awaitable, Type, TypeVar

import httpx
from httpx import AsyncClient
from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    status: int
    message: str
    timestamp: Optional[int] = None
    code: str
    error: Optional[str] = Field(default=None, hidden=True)

    def model_dump(self, **kwargs):
        data: dict = super().model_dump(**kwargs)

        if data["error"] is None:
            del data["error"]

        return data

    class Config:
        @staticmethod
        def json_schema_extra(schema: dict, _):
            """Via https://github.com/tiangolo/fastapi/issues/1378"""
            props = {}
            for k, v in schema.get('properties', {}).items():
                if not v.get("hidden", False):
                    props[k] = v
            schema["properties"] = props

    def verify(self) -> "BaseResponse":
        """Will throw an error if the status is not successful"""

        if self.code != "SUCCESS":
            raise CriadexError(bad_response=self)

        return self


class CriadexError(RuntimeError):
    """Thrown when """

    def __init__(self, bad_response: BaseResponse):
        self.response = self.bad_response = bad_response


T = TypeVar('T', bound=BaseResponse)


def reshape(payload: dict, model: Type[T]) -> T:
    if not issubclass(model, BaseResponse):
        raise ValueError("Model must subclass the base response type.")
    try:
        return model(**payload)
    except (ValueError, TypeError):
        # This is thrown in the case of catastrophic error
        # The payload by definition will not match an expected shape
        # The best we can do is print the payload & trace so the user knows what's up
        return BaseResponse(
            code="SERIALIZE_ERROR",
            status=500,
            message=f"Serialization error! Payload: {payload} | Exception: {traceback.format_exc()}"
        )


def outputs(model: Type[T]) -> Callable[[Callable], Callable[..., Awaitable[T]]]:
    def decorator(function: Callable[..., Awaitable[T]]) -> Callable:
        @wraps(function)
        async def wrapper(self, *args, **kwargs) -> T:
            result: Optional[dict] = await function(self, *args, **kwargs)

            return reshape(
                model=model,
                payload=result
            )

        return wrapper

    return decorator


class Route:

    def __init__(
            self,
            http: AsyncClient,
            api_base: str
    ):
        self._http: AsyncClient = http
        self._api_base: str = api_base

    class Response(BaseResponse):
        pass

    def __call__(self, **kwargs) -> Awaitable:
        return self.execute(**kwargs)

    @abstractmethod
    async def execute(self, **kwargs) -> Optional[dict]:
        raise NotImplementedError

    @classmethod
    async def __base_request(cls, method: Callable[[], Awaitable[httpx.Response]]) -> Optional[dict]:
        try:
            result: httpx.Response = await method()
            if os.environ.get("CRIADEX_SDK_REQUEST_DEBUG_ENABLED", "").lower() == "true":
                print("-- Response Debug ---")
                print("Code:", str(result))
                print("Content:", result.read())
            return result.json()
        except Exception:
            logging.error("Criadex Request Error: " + traceback.format_exc())
            return None

    def __build_url(self, path: str) -> str:
        return self._api_base + (path if path.startswith("/") else "/" + path)

    async def _generic_request(self, http_fn: Callable, path: str, **kwargs) -> Optional[dict]:
        return await self.__base_request(
            functools.partial(
                http_fn,
                self.__build_url(path),
                **self.de_pydantic(kwargs)
            )
        )

    async def _get(self, path: str, **kwargs) -> Optional[dict]:
        return await self._generic_request(self._http.get, path, **kwargs)

    async def _post(self, path: str, **kwargs) -> Optional[dict]:
        return await self._generic_request(self._http.post, path, **kwargs)

    async def _patch(self, path: str, **kwargs) -> Optional[dict]:
        return await self._generic_request(self._http.patch, path, **kwargs)

    async def _delete(self, path: str, **kwargs) -> Optional[dict]:
        return await self._generic_request(self._http.delete, path, **kwargs)

    @classmethod
    def de_pydantic(cls, obj: dict[str, Any]):

        if isinstance(obj, BaseModel):
            return obj.model_dump()

        for k, v in obj.items():
            if isinstance(v, dict):
                obj[k] = cls.de_pydantic(v)

            if isinstance(v, list):
                obj[k] = [cls.de_pydantic(i) for i in obj[k]]

        for k, v in obj.items():
            if isinstance(v, BaseModel):
                obj[k] = v.model_dump()

        return obj
