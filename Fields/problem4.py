from pydantic import BaseModel, Field

# Create a model Employee with:
# emp_id → int, positive, with description="Employee ID"
# name → string, min length 2
# salary → float, ge 10000
# Add example data for all fields


class Employee(BaseModel):
    emp_id: int = Field(gt=0, description="Employee ID", examples=[202201])
    name: str = Field(min_length=2, examples=["harsh patel"])
    salary: float = Field(ge=10000, examples=[120000])


emp1 = Employee(emp_id=202202, name="raj kumar", salary=232342)
print(emp1)
