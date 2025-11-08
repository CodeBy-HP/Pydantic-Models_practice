from pydantic import BaseModel, Field, EmailStr


class Address(BaseModel):
    street: str
    city: str
    zip: str = Field(..., pattern=r"\d{6}")


class User(BaseModel):
    name: str
    email: EmailStr
    address: Address


u1 = User(
    name="Harsh Patel",
    email="harsh@gmail.com",
    address=Address(street="MG Road", city="Pune", zip="411001"),
)
print(u1)
