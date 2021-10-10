from decimal import Decimal
from typing import Optional, List

from pydantic.main import BaseModel


class Category(BaseModel):
    id: Optional[int]
    category_name: str


class PostCategory(BaseModel):
    category_name: str


class Drug(BaseModel):
    id: Optional[int]
    name: str
    category_id: int
    description: Optional[str]
    prescription: bool
    price: Decimal


class PostDrug(BaseModel):
    name: str
    category_id: int
    description: Optional[str]
    prescription: bool
    price: Decimal


class ResponseCategories(BaseModel):
    data: List[Category]


class ResponseCategory(BaseModel):
    data: Category


class ResponseDrugs(BaseModel):
    data: List[Drug]


class ResponseDrug(BaseModel):
    data: Drug


class ResponseUpdate(BaseModel):
    details: str
