from typing import Optional
from pydantic import BaseModel, Field, Extra


class AddressSchenma(BaseModel):
    city: str
    country: str


class SocialsSchema(BaseModel):
    type: str
    link: str


class UserCreateSchema(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(gt=0)
    address: AddressSchenma
    phoneNum: list[str] = Field(min_items=1)
    socials: list[SocialsSchema] = Field(min_items=1)

    class Config:
        extra = Extra.forbid

class UserUpdateSchema(BaseModel):
    name: Optional[str] = Field(min_length=2, max_length=50)
    age: Optional[int] = Field(gt=0)
    address: Optional[AddressSchenma]
    phoneNum: Optional[list[str]] = Field(min_items=1)
    socials: Optional[list[SocialsSchema]] = Field(min_items=1)

    class Config:
        extra = Extra.forbid


def ResponseModel(data, message):
    return {
        "data": data or None,
        "statusCode": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    print("error is", error)
    return {"error": error, "statusCode": code, "message": message}            
