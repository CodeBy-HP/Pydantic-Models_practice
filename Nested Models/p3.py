from pydantic import BaseModel, Field
from typing import Optional

# Make a model UserProfile that has:
# name, age, address: Address | None
# Ensure address can be missing but if present, its city and zip are required.


class Address(BaseModel):
    city: str
    zip: str = Field(..., pattern=r"\d{6}")


class UserProfile(BaseModel):
    name: str
    age: int
    address: Optional[Address] = None

u2 = UserProfile(
    name="Raj",
    age=25,
    address=Address(city="Pune", zip="411001")
)
print(u2)
