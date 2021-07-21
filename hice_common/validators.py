import re


class ValidationError(ValueError):
    """
    Exception that raises if passed data is invalid
    """
    pass


def validate_phone_number(phone_number: str) -> str:

    if not isinstance(phone_number, str):
        raise ValidationError('phone_number should be passed as string')

    digits = ''.join(c for c in phone_number if c.isdigit())
    if len(digits) < 9 or len(digits) > 12:
        raise ValidationError('wrong size of phone number, it can be bettwen 10 and 11')
    digits = f'7{digits[-10:]}'

    if re.match(r'^79\d{9}$', digits) is None:
        raise ValidationError('wrong value of phone number, it can be bettwen 10 and 11')
    return digits
