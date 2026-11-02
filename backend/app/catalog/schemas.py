from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
    name: str
    category: str
    description: str
    details: list[str]
    price: Decimal = Field(ge=0)
    inventory: int = Field(ge=0)
    imageUrl: str
    accent: str
    featured: bool = False

