from pydantic import BaseModel, Field, model_validator

# Create a Product model with:
# name: str
# price: float
# Use a before validator to:
# Automatically strip whitespace from name
# Convert price to float even if user passes "499.99" as a string


class Product(BaseModel):
    name: str
    price: float

    @model_validator(mode="before")
    def process(cls, data):
        if isinstance(data, dict):
            data["name"] = data["name"].strip()
            data["price"] = float(data["price"])
        return data


p1 = Product(name="  Laptop  ", price="499.99")
print(p1)
