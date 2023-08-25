from typing import Union

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: Union[str, None] = None
    price: int


class ProductCreate(ProductBase):
    owner_id: int


class ProductUpdate(ProductBase):
    pass


class ProductScheme(ProductBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
