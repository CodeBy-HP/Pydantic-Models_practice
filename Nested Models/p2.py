from pydantic import BaseModel, Field, model_validator
from typing import List

# Create models:
# Item → name, price (> 0)
# Order → order_id, items: list[Item], total: float
# Validate that:
# total ≥ sum of item prices
# (Hint: use model_validator for cross-field validation)


class Item(BaseModel):
    name: str
    price: int = Field(gt=0)


class Order(BaseModel):
    order_id: int
    items: List[Item]
    total: float

    @model_validator(mode="after")
    def check_total(self):
        total_price = sum(item.price for item in self.items)
        if self.total < total_price:
            raise ValueError(
                f"Total {self.total} is less than the sum of items prices {total_price}"
            )
        return self


o2 = Order(
    order_id=102,
    items=[Item(name="Book", price=200), Item(name="Pen", price=50)],
    total=100,
)

print(o2)
