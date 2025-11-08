from pydantic import BaseModel, EmailStr


# Create model Customer with:
# name: string
# email: optional string
# If email is missing → it defaults to "not_provided@example.com"

class Customer(BaseModel):
    name: str
    email: EmailStr = "not_provided@example.com"


c1 = Customer(name="harsh")

print(c1)
