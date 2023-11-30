from pydantic import EmailStr, BaseModel
from fastapi_users import schemas
from fastapi_users.schemas import CreateUpdateDictModel, PYDANTIC_V2
from pydantic import ConfigDict


class UserRead(CreateUpdateDictModel):

    email: EmailStr

    if PYDANTIC_V2:
        model_config = ConfigDict(from_attributes=True)
    else:

        class Config:
            orm_mode = True


class UserCreate(CreateUpdateDictModel):

    email: EmailStr
    password: str


class UserUpdate(schemas.BaseUserUpdate):
    pass


class Title(BaseModel):

    id: int
    name: str
    url: str
    remote_path: str
