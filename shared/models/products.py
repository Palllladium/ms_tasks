from sqlmodel import (
    SQLModel, 
    Text, 
    DateTime, 
    Field
)
from typing import Optional
from pydantic import ConfigDict
from datetime import datetime as dt, timezone


class ProductBase(SQLModel):
    model_config = ConfigDict(from_attributes=True)
    product_name: str = Field(max_length=100)
    product_description: str = Field(sa_type=Text)
    count_left: int = Field(ge=0)
    create_time: dt = Field(
        default_factory=lambda: dt.now(timezone.utc),
        sa_type=DateTime(timezone=True)
    )
    update_time: dt = Field(
        default_factory=lambda: dt.now(timezone.utc),
        sa_type=DateTime(timezone=True)
    )


class Product(ProductBase, table=True):
    __tablename__ = "products"
    product_id: Optional[int] = Field(default=None, primary_key=True)