from pydantic import BaseModel, Field, model_validator
from typing import Annotated, List, Optional

# Create a model ShoppingList with:
# items: list of strings, must have at least 2 items
# total_items: integer (auto-calculated using model_validator — should equal length of items)


class ShoppingList(BaseModel):
    items: Annotated[List[str], Field(min_length=2)]
    total_items: Optional[int] = None

    @model_validator(mode="after")
    def set_total_items(self):
        self.total_items = len(self.items)
        return self


s = ShoppingList(items=["milk", "bread", "butter"])
print(s)
