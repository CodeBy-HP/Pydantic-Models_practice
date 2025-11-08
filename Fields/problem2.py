from pydantic import BaseModel, Field
from typing import Required, Optional

# Create a model UserProfile with:
# username → string, min length 4, max length 20
# email → required string
# bio → optional string, default empty "", max length 150
# age → integer, default 18, must be ≥ 13

# Optional Simply means that the Attribute could be None


class UserProfile(BaseModel):
    username: str = Field(min_length=4, max_length=20)
    email: str  # required
    bio: Optional[str] = Field(default="", max_length=150)
    age: int = Field(default=18, ge=13)


user1 = UserProfile(username="harsh", email="code@gmail.com")
print(user1)
