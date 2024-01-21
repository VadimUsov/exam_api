from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional


class Category(BaseModel):
    id: int
    name: str


class Tags(BaseModel):
    id: int
    name: str


class Pet(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id: Optional[int] = None
    category: Optional[Category] = None
    name: str
    photoUrls: list[str] = Field(alias="photoUrls")
    tags: Optional[list[Tags]] = None
    status: Optional[str] = None

    @field_validator("status")
    @classmethod
    def check_status(cls, value) -> str:
        statuses = ["available", "pending", "sold"]
        if value in statuses:
            return value
        raise ValueError("This is incorrect status")

