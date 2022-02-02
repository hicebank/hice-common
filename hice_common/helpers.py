import asyncio
from collections import defaultdict
from datetime import datetime, date
from decimal import Decimal
from functools import wraps
from typing import Any, Union, Dict, List, Callable, Tuple, Optional, Coroutine
from uuid import UUID


def to_json_serializable(
    data: Any
) -> Union[Dict[str, Any], List[Dict[str, Any]], List[str], str]:
    if isinstance(data, (datetime, date)):
        return data.isoformat()
    elif isinstance(data, Decimal):
        return str(data)
    elif isinstance(data, UUID):
        return str(data)
    elif isinstance(data, list):
        for i in range(len(data)):
            data[i] = to_json_serializable(data[i])
        return data
    elif isinstance(data, dict):
        for key in data:
            data[key] = to_json_serializable(data[key])
        return data
    return data


def cache_function(expire: int = 60 * 60) -> Callable[
    [Callable[..., Union[Coroutine[Any, Any, Any], Any]]],
    Callable[..., Union[Coroutine[Any, Any, Any], Any]]
]:
    def decorator(
        func: Callable[[Any, Any], Union[Coroutine[Any, Any, Any], Any]]
    ) -> Callable[[Any, Any], Union[Coroutine[Any, Any, Any], Any]]:
        cache_value: Dict[Tuple[Any, frozenset], Any] = defaultdict(lambda: None)
        last_call: Dict[Tuple[Any, frozenset], Optional[datetime]] = defaultdict(lambda: None)

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (args, frozenset(sorted(kwargs.items())))
            current_value = cache_value[key]
            last_call_value = last_call[key]
            if (
                current_value is None
                or (last_call_value is not None and (datetime.utcnow() - last_call_value).total_seconds() > expire)
            ):
                try:
                    value = await func(*args, **kwargs)  # type: ignore
                except Exception as e:
                    if current_value is not None:
                        # add logging that was exception and we return cached value
                        return current_value
                    raise e
                else:
                    cache_value[key] = value
                    last_call[key] = datetime.utcnow()
            return cache_value[key]

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (args, frozenset(sorted(kwargs.items())))
            current_value = cache_value[key]
            last_call_value = last_call[key]
            if (
                current_value is None
                or (last_call_value is not None and (datetime.utcnow() - last_call_value).total_seconds() > expire)
            ):
                try:
                    value = func(*args, **kwargs)  # type: ignore
                except Exception as e:
                    if current_value is not None:
                        # add logging that was exception and we return cached value
                        return current_value
                    raise e
                else:
                    cache_value[key] = value
                    last_call[key] = datetime.utcnow()
            return cache_value[key]

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator
