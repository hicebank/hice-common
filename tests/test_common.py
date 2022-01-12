import pytest
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError

from hice_common import validate_phone_number, PhoneNumber
from hice_common import ValidationError as PhoneNumberValidationError


class PhoneNumberModel(BaseModel):
    phone_number: PhoneNumber


@pytest.mark.parametrize('test_input,expected', [
    ('89222120919', '79222120919'),
    ('9222120919', '79222120919'),
    ('79222120919', '79222120919'),
    ('+79222120919', '79222120919'),
    ('+9222120919', '79222120919'),
    ('+7(922)212-09-19', '79222120919'),
    ('+7 (922) 212 - 09 - 19', '79222120919'),
    ('(922) 212 - 09 - 19', '79222120919'),
    (' (922) 212 - 09 - 19', '79222120919'),
    ('8 (922) 212 - 09 - 19', '79222120919'),
    ('8(922)212-09-19', '79222120919'),
    ('7(922)212-09-19', '79222120919'),
    ('(922)212-09-19', '79222120919'),
])
def test_valid_phone_number(test_input: str, expected: str) -> None:
    """No exception raise"""
    assert validate_phone_number(test_input) == expected

    phone_number_model = PhoneNumberModel(phone_number=test_input)
    assert phone_number_model.phone_number == expected


@pytest.mark.parametrize('phone_number', [
    None,
    '',
    79292225517,
    79292,
    '7929222551',
    '8929222551',
    '792922225517',
    '892922225517',
    '7929ooo2217',
])
def test_wrong_phone_number(phone_number):
    with pytest.raises(PhoneNumberValidationError):
        validate_phone_number(phone_number)

    with pytest.raises(PydanticValidationError):
        PhoneNumberModel(phone_number=phone_number)

    with pytest.raises(PydanticValidationError):
        PhoneNumberModel(phone_number=phone_number)

    with pytest.raises(PydanticValidationError):
        PhoneNumberModel(phone_number=phone_number)
