from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class EventInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    event_id: UUID
    kind: Literal["impression", "click", "view", "search", "add_to_cart", "remove_from_cart"]
    product_id: UUID | None = None
    query: str | None = Field(default=None, max_length=200)

    @model_validator(mode="after")
    def check_target(self):
        if self.kind == "search":
            if not self.query or not self.query.strip():
                raise ValueError("Search events require a query")
        elif self.product_id is None:
            raise ValueError("Product events require product_id")
        return self
