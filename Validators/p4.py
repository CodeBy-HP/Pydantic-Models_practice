from pydantic import BaseModel, Field, model_validator

# Create a Register model with:
# password: str
# confirm_password: str
# Add a model_validator(mode='after') that ensures:
# password == confirm_password, else raise "Passwords do not match".


class Register(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def validate_pass(cls, self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


r1 = Register(password="123", confirm_password="123")
print(r1)
