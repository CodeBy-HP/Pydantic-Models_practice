# 🤖 Pydantic V2 Essentials for FastAPI

**Pydantic** enforces **data shape** and **validation** for Python code using Python's native type annotations. It's the core of request and response handling in **FastAPI**.

---

## 1. Defining a Simple Model

Use \`BaseModel\` to define data structures.

\`\`\`python
from pydantic import BaseModel

# Defines a structure for a Product

class Product(BaseModel): # Field type enforced: must be str
name: str # Field type enforced: must be integer
quantity: int = 1 # Default value
\`\`\`

---

## 2. Model Fields and Constraints (Field & Annotated)

The \`Field\` function adds constraints, validation rules, and metadata.  
\`Annotated\` is the clean, modern way to apply these in Pydantic v2.

\`\`\`python
from pydantic import BaseModel, Field
from typing import Annotated # Modern way to add metadata/constraints

class Item(BaseModel): # Required field, min/max length constraint
name: Annotated[str, Field(min_length=3, max_length=50)]

    # Must be positive and less than 10000
    price: Annotated[float, Field(gt=0, lt=10000, description="Price must be positive")]

    # Required field with an alternate name for input/output
    user_alias: str = Field(..., alias="userName")

# Usage Example:

# item = Item(userName="Widget A", price=9.99)

\`\`\`

| Parameter                  | Meaning                                  | Example                         |
| -------------------------- | ---------------------------------------- | ------------------------------- |
| \`...\`                    | Required field (no default)              | \`Field(...)\`                  |
| \`gt, lt, ge, le\`         | Greater/Less than constraints            | \`Field(gt=0)\`                 |
| \`min_length, max_length\` | Length constraints                       | \`Field(min_length=3)\`         |
| \`alias\`                  | Alternate key name for input/output      | \`Field(alias="user_name")\`    |
| \`default_factory\`        | Dynamic default value (e.g., list, dict) | \`Field(default_factory=list)\` |

---

## 3. Nested Models

Models can contain other models, enabling structured, validated data hierarchies.

\`\`\`python
from pydantic import BaseModel

# Nested Model

class Address(BaseModel):
city: str
zip: str

# Primary Model

class User(BaseModel):
name: str
address: Address # Nested: Address is required
billing: Address | None = None # Optional Nested: Address or None

# Example Input (automatically validated):

# data = {"name": "Alice", "address": {"city": "Indore", "zip": "452001"}}

\`\`\`

---

## 4. Collections and Advanced Types

Use standard Python typing for lists, dictionaries, optional fields, and multiple valid types.

\`\`\`python
from pydantic import BaseModel
from typing import List, Dict, Union, Optional

class Profile(BaseModel): # List of strings (all elements are validated)
tags: List[str]

    # Dictionary with string keys and values that are str or int
    preferences: Dict[str, Union[str, int]]

    # Field can be str or None (Optional[str] is the same)
    phone: Optional[str] = None

\`\`\`

| Type              | Meaning                   | Example               |
| ----------------- | ------------------------- | --------------------- | ----------------- |
| \`List[T]\`       | List of type T            | \`List[str]\`         |
| \`Dict[K, V]\`    | Key-value pairs           | \`Dict[str, int]\`    |
| \`T               | None\` or \`Optional[T]\` | Can be type T or None | \`Optional[str]\` |
| \`Union[T1, T2]\` | Either T1 or T2 allowed   | \`Union[int, float]\` |

---

## 5. Model Methods (V2 Replacements)

Pydantic v2 introduces new, clearer method names for common tasks.

\`\`\`python
from pydantic import BaseModel

class Data(BaseModel):
key: str
value: int

d = Data(key="test", value=100)

# Convert to Python dict (Replaces .dict() from v1)

data_dict = d.model_dump()

# {'key': 'test', 'value': 100}

# Convert to JSON string (Replaces .json() from v1)

data_json = d.model_dump_json()

# '{"key":"test","value":100}'

# Create a copy (Replaces .copy() from v1)

d_copy = d.model_copy(update={"value": 200})

# Create from external dict/JSON (Replaces .parse_obj()/.parse_raw() from v1)

d_from_dict = Data.model_validate({"key": "new", "value": 50})
\`\`\`

---

## 6. Field Validators (@field_validator)

Runs logic on a single field after or before type validation. (Replaces \`@validator\` from v1).

\`\`\`python
from pydantic import BaseModel, field_validator

class User(BaseModel):
name: str
age: int

    # Validator for the 'age' field
    @field_validator('age')
    def age_must_be_adult(cls, v):
        if v < 18:
            raise ValueError('User must be 18 or older')
        return v

\`\`\`

---

## 7. Model Validators (@model_validator)

Runs logic on the entire model to validate cross-field constraints. (Replaces \`@root_validator\` from v1).

\`\`\`python
from pydantic import BaseModel, model_validator

class Account(BaseModel):
password: str
confirm_password: str

    # Runs after all fields are validated. Accesses fields via 'self'.
    @model_validator(mode='after')
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        # Must return self!
        return self

\`\`\`

---

## 8. Computed Fields

Fields whose value is calculated dynamically from other fields. They are read-only and included in \`model_dump()\`.

\`\`\`python
from pydantic import BaseModel, computed_field

class Product(BaseModel):
price: float
tax_rate: float # e.g., 0.18 for 18%

    @computed_field
    @property
    def total_price(self) -> float:
        return self.price * (1 + self.tax_rate)

# p = Product(price=100, tax_rate=0.18)

# p.model_dump() -> {'price': 100, 'tax_rate': 0.18, 'total_price': 118.0}

\`\`\`

---

## 9. Generic Models

Define a reusable container structure where the inner type is a placeholder. Great for standardized API responses.

\`\`\`python
from pydantic import BaseModel
from typing import TypeVar, Generic, List

T = TypeVar('T')

# The Generic Response Wrapper

class Response(Generic[T], BaseModel):
data: T
success: bool

class User(BaseModel):
username: str

# Create a specialized response for a list of Users

ResponseListUsers = Response[List[User]]

# response_data = ResponseListUsers(data=[...], success=True)

\`\`\`

