from pydantic import BaseModel, Field, model_validator, field_validator


# Create a Transaction model with:
# sender_balance: float
# amount: float
# receiver_balance: float
# Validations:
# Field validator: amount must be > 0
# Model validator: ensure sender_balance - amount ≥ 0,
# else raise "Insufficient funds"


class Transaction(BaseModel):
    sender_balance: float
    amount: float
    receiver_balance: float

    @field_validator("amount")
    def amount_check(cls, v):
        if v <= 0:
            raise ValueError("Amount must be > 0")
        return v

    @model_validator(mode="after")
    def validate_sender_balance(cls, self):
        if (self.sender_balance - self.amount) < 0:
            raise ValueError("Insufficient funds")
        return self


t1 = Transaction(sender_balance=500, amount=200, receiver_balance=0)
print(t1)
