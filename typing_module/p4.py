from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict, Union, Optional, Annotated

# Create model Profile with:
# username: str
# skills: list of strings (min 1)
# settings: dict with keys = str, values = str or int
# contact: optional dict with phone and email (both strings)


class Contact(BaseModel):
    phone: str
    email: EmailStr


class Profile(BaseModel):
    username: str
    skills: Annotated[List[str], Field(min_length=1)]
    settings: Dict[str, Union[str, int]]
    contact: Optional[Contact] = None


p = Profile(
    username="harsh",
    skills=["Python", "Docker"],
    settings={"theme": "dark", "level": 5},
    contact=Contact(phone="9876543210", email="harsh@example.com"),
)
print(p)
