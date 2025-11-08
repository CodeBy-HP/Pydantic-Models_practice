from pydantic import BaseModel, Field, field_validator

# Create a Person model with fields:
# name: str
# age: int
# Validate that:
# age must be between 1 and 120 (inclusive).
# If invalid, raise "Invalid age range".


class Person(BaseModel):
    name: str
    age: int

    @field_validator("age")
    def check(cls, value):
        if not (1 <= value <= 120):
            raise ValueError("the age must be between 1 and 120")
        return value


p1 = Person(name="harsh", age=120)
print(p1)
