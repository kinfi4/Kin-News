from pydantic import BaseModel, root_validator, Field


class UserEntity(BaseModel):
    username: str
    password: str


class UserRegistrationEntity(BaseModel):
    username: str
    password: str
    password_repeated: str = Field(..., alias='passwordRepeated')

    @root_validator()
    def validate_passwords_equal(cls, fields: dict[str, str]) -> dict[str, str]:
        password1, password2 = fields.get('password'), fields.get('password_repeated')
        if password1 is None or password2 is None or password1 != password2:
            raise ValueError('Passwords must be equal!')

        return fields

    class Config:
        allow_population_by_field_name = True
