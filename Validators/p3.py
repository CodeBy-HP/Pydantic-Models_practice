from pydantic import BaseModel, Field, field_validator

# Create a Student model with:
# roll_no: int
# name: str
# grade: str
# Use one field validator that runs on both name and grade,
# and ensures neither are empty or blank.


class Student(BaseModel):
    roll_no: int
    name: str
    grade: str

    @field_validator("name", "grade")
    def validate_not_blank(cls, v):
        if not v or not v.strip():
            raise ValueError("Field cannot be empty or blank")
        return v


s1 = Student(roll_no=1, name="Harsh", grade="A")
print(s1)
