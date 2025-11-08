from pydantic import BaseModel, Field
from typing import Annotated

# Create a model Vehicle with:
# plate_number → must match pattern ^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$ (e.g., MH12AB1234)
# model_name → min length 2, max length 30
# price → float, > 50000


class Vehicle(BaseModel):
    plate_number: Annotated[str, Field(pattern=r"^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$")]
    model_name: Annotated[str, Field(min_length=2, max_length=30)]
    price: Annotated[float, Field(gt=50000)]


vh = Vehicle(plate_number="MH12AB1234", model_name="Maruti", price=120000)

print(vh)
