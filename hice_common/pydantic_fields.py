from typing import Any, Callable, Generator

from .validators import ValidationError, validate_phone_number

try:
    from pydantic.errors import PydanticValueError
except ImportError:
    pass

CallableGenerator = Generator[Callable[..., Any], None, None]


class PydanticValidationError(PydanticValueError):
    msg_template = 'invalid {name}: {reason}'


def _validate_wrapper(func: Callable[[str], str], name: str, value: str) -> str:
    try:
        result = func(value)
    except ValidationError as e:
        raise PydanticValidationError(name=name, reason=str(e))

    return result


class PhoneNumber(str):
    @classmethod
    def __get_validators__(cls) -> CallableGenerator:
        yield cls.validate

    @classmethod
    def validate(cls, value: str) -> str:
        return _validate_wrapper(validate_phone_number, "phone_number", value)
