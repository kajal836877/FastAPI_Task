from pydantic import BaseModel, Field
from typing import Literal


class ItemCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=5)
    category: str = Field(min_length=1)
    location: str = Field(min_length=1)
    reported_by: str = Field(min_length=1)
    status: Literal["Lost", "Found", "Returned"]


class ItemUpdate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=5)
    category: str = Field(min_length=1)
    location: str = Field(min_length=1)
    reported_by: str = Field(min_length=1)
    status: Literal["Lost", "Found", "Returned"]
    