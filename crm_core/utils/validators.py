from pydantic import BaseModel, validator
from typing import Optional


class EmailValidator(BaseModel):
    email: str

    @validator('email')
    def email_must_be_valid(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v


def validate_cpf(cpf: str) -> bool:
    # Basic CPF validation (Brazilian ID)
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    # Add more validation logic here
    return True


def validate_phone(phone: str) -> bool:
    # Basic phone validation
    if len(phone) < 10 or not phone.isdigit():
        return False
    return True
