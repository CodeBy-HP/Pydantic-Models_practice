from pydantic import BaseModel, Field
from typing import Annotated

# Create a model Book with:
# title → required string, min length 3
# pages → positive integer (must be > 0)
# price → float, must be between 10 and 1000


class Book(BaseModel):
    title: Annotated[str, Field(min_length=3)]
    pages: Annotated[int, Field(gt=0)]
    price: Annotated[float, Field(ge=10, le=1000)]


# Valid example
ob1 = Book(title="Beyond Good and Evil", pages=250, price=100)
ob2 = Book(title="ANY BOOK", pages=23, price=2) 
# error - Input should be greater than or equal to 10

print(ob1)
