from pydantic import BaseModel, Field
from typing import Union, Dict

# Create model Settings with:
# config: dict where key = string, value = int or bool
# Example:
# {"retries": 3, "verbose": True} should be valid.


class Settings(BaseModel):
    config: Dict[str, Union[int, bool]]


d1 = {"retries": 3, "verbose": True}
s1 = Settings(config=d1)
print(s1)
