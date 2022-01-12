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
    if not 9 < len(digits) < 12:
        raise ValidationError('wrong size of phone number, it can be between 10 and 11')

    if (digits.startswith('9') and len(digits) == 10) or (digits.startswith('8') and len(digits) == 11):
        digits = f'7{digits[-10:]}'

    if re.match(r'^79\d{9}$', digits) is None:
        raise ValidationError('phone number must start from 79')

    return digits
