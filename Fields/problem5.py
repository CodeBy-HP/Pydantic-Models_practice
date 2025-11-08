from pydantic import BaseModel, Field
from typing import List

# Create a model Cart with:
# items → list of strings, default to empty list (using default_factory)
# total → float, default 0.0, must be ≥ 0


class Cart(BaseModel):
    items: List[str] = Field(default_factory=list)
    total: float = Field(default=0.0, ge=0)


# default_factory=list means: “if no value is provided, create a new empty list.”
# If you used default=[], all instances would share the same list (mutable default trap).
# That’s why default_factory is preferred for lists, dicts, sets, etc.

c1 = Cart(items=["eraser", "pencil"], total=2323)
print(c1)
