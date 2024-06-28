from pydantic import BaseModel, EmailStr, Field

from config import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ProductSchema(BaseModel):
    title: str = Field(default=None)
    description: str = Field(default=None)
    price: int = Field(default=None)

    class Config:
        schema_extra = {
            "product_demo": {
                "id": 1,
                "title": "football",
                "description": "GOAT",
                "price": 1
            }
        }


class UserSchema(BaseModel):
    fullname: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)

    class Config:
        user_schema = {
            "user_example": {
                "name": "abduvali",
                "email": "murodullayevabduvali972@gmail.com",
                "password": "12"

            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)

    class Config:
        user_schema = {
            "user_example": {
                "email": "murodullayevabduvali972@gmail.com",
                "password": "12"

            }
        }
