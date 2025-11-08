# Pydantic V2 - Complete Guide

A comprehensive guide to Pydantic V2 for data validation and settings management using Python type hints.

## Table of Contents
- [Installation](#installation)
- [Basic Models](#basic-models)
- [Fields & Validation](#fields--validation)
- [Field Types](#field-types)
- [Validators](#validators)
- [Nested Models](#nested-models)
- [Advanced Typing](#advanced-typing)
- [Model Configuration](#model-configuration)
- [Serialization](#serialization)
- [Advanced Features](#advanced-features)

---

## Installation

```bash
pip install pydantic
pip install "pydantic[email]"  # For EmailStr support
```

---

## Basic Models

Pydantic models are Python classes that inherit from `BaseModel`:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str

# Create instance
user = User(name="John", age=30, email="john@example.com")
print(user)
# Output: name='John' age=30 email='john@example.com'
```

**Key Features:**
- Automatic type validation
- Data parsing and conversion
- Clear error messages
- IDE autocompletion support

---

## Fields & Validation

### Field Constraints

Use `Field` for detailed validation rules:

```python
from pydantic import BaseModel, Field
from typing import Annotated

class Book(BaseModel):
    title: Annotated[str, Field(min_length=3)]
    pages: Annotated[int, Field(gt=0)]
    price: Annotated[float, Field(ge=10, le=1000)]

book = Book(title="Beyond Good and Evil", pages=250, price=100)
```

**Common Field Constraints:**
- `min_length`, `max_length` - String/list length
- `gt`, `ge`, `lt`, `le` - Numeric comparisons (greater than, greater or equal, etc.)
- `pattern` - Regex pattern matching
- `default` - Default value
- `default_factory` - Factory function for mutable defaults

### Required vs Optional Fields

```python
from typing import Optional

class UserProfile(BaseModel):
    username: str = Field(min_length=4, max_length=20)
    email: str  # Required
    bio: Optional[str] = Field(default="", max_length=150)
    age: int = Field(default=18, ge=13)
```

**Note:** `Optional[str]` means the field can be `None`, not that it's optional to provide.

### Pattern Matching

```python
class Vehicle(BaseModel):
    plate_number: Annotated[str, Field(pattern=r"^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$")]
    model_name: Annotated[str, Field(min_length=2, max_length=30)]
    price: Annotated[float, Field(gt=50000)]

# Valid: MH12AB1234
vehicle = Vehicle(plate_number="MH12AB1234", model_name="Maruti", price=120000)
```

### Field Metadata

```python
class Employee(BaseModel):
    emp_id: int = Field(gt=0, description="Employee ID", examples=[202201])
    name: str = Field(min_length=2, examples=["John Doe"])
    salary: float = Field(ge=10000, examples=[120000])
```

### Default Factory

Use `default_factory` for mutable defaults (lists, dicts):

```python
from typing import List

class Cart(BaseModel):
    items: List[str] = Field(default_factory=list)
    total: float = Field(default=0.0, ge=0)

# Each instance gets its own list
cart1 = Cart()
cart2 = Cart()
```

---

## Field Types

### Email Validation

```python
from pydantic import EmailStr

class Customer(BaseModel):
    name: str
    email: EmailStr = "not_provided@example.com"

customer = Customer(name="Alice", email="alice@example.com")
```

### Common Types
- `str`, `int`, `float`, `bool` - Basic types
- `EmailStr` - Email validation
- `HttpUrl` - URL validation
- `UUID` - UUID validation
- `datetime`, `date`, `time` - Date/time types
- `Path`, `FilePath`, `DirectoryPath` - File system paths

---

## Validators

### Field Validators

Validate individual fields using `@field_validator`:

```python
from pydantic import field_validator

class Person(BaseModel):
    name: str
    age: int

    @field_validator("age")
    def validate_age(cls, value):
        if not (1 <= value <= 120):
            raise ValueError("Age must be between 1 and 120")
        return value
```

**Multiple Field Validation:**

```python
class Student(BaseModel):
    roll_no: int
    name: str
    grade: str

    @field_validator("name", "grade")
    def validate_not_blank(cls, v):
        if not v or not v.strip():
            raise ValueError("Field cannot be empty or blank")
        return v
```

### Model Validators

#### Before Mode (Pre-processing)

Runs before Pydantic's own validation:

```python
from pydantic import model_validator

class Product(BaseModel):
    name: str
    price: float

    @model_validator(mode="before")
    def process_data(cls, data):
        if isinstance(data, dict):
            data["name"] = data["name"].strip()
            data["price"] = float(data["price"])
        return data

product = Product(name="  Laptop  ", price="499.99")
```

#### After Mode (Post-processing)

Runs after all field validations:

```python
from typing import Optional, List

class ShoppingList(BaseModel):
    items: Annotated[List[str], Field(min_length=2)]
    total_items: Optional[int] = None

    @model_validator(mode="after")
    def set_total_items(self):
        self.total_items = len(self.items)
        return self
```

#### Cross-Field Validation

```python
class Register(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def validate_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
```

### Combining Validators

```python
class Transaction(BaseModel):
    sender_balance: float
    amount: float
    receiver_balance: float

    @field_validator("amount")
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("Amount must be > 0")
        return v

    @model_validator(mode="after")
    def validate_balance(self):
        if (self.sender_balance - self.amount) < 0:
            raise ValueError("Insufficient funds")
        return self
```

---

## Nested Models

### Basic Nesting

```python
class Address(BaseModel):
    street: str
    city: str
    zip: str = Field(..., pattern=r"\d{6}")

class User(BaseModel):
    name: str
    email: EmailStr
    address: Address

user = User(
    name="Harsh Patel",
    email="harsh@gmail.com",
    address=Address(street="MG Road", city="Pune", zip="411001")
)
```

### Optional Nested Models

```python
class UserProfile(BaseModel):
    name: str
    age: int
    address: Optional[Address] = None

# Without address
user1 = UserProfile(name="John", age=25)

# With address
user2 = UserProfile(
    name="Jane",
    age=30,
    address=Address(street="Main St", city="Mumbai", zip="400001")
)
```

### Complex Nested Structures

```python
class Item(BaseModel):
    name: str
    price: int = Field(gt=0)

class Order(BaseModel):
    order_id: int
    items: List[Item]
    total: float

    @model_validator(mode="after")
    def validate_total(self):
        total_price = sum(item.price for item in self.items)
        if self.total < total_price:
            raise ValueError(f"Total {self.total} is less than sum of items")
        return self

order = Order(
    order_id=101,
    items=[Item(name="Book", price=200), Item(name="Pen", price=50)],
    total=250
)
```

---

## Advanced Typing

### Union Types

```python
from typing import Union, Dict

class Settings(BaseModel):
    config: Dict[str, Union[int, bool]]

settings = Settings(config={"retries": 3, "verbose": True})
```

### Complex Type Combinations

```python
from typing import List, Dict, Union, Optional

class Contact(BaseModel):
    phone: str
    email: EmailStr

class Profile(BaseModel):
    username: str
    skills: Annotated[List[str], Field(min_length=1)]
    settings: Dict[str, Union[str, int]]
    contact: Optional[Contact] = None

profile = Profile(
    username="harsh",
    skills=["Python", "Docker"],
    settings={"theme": "dark", "level": 5},
    contact=Contact(phone="9876543210", email="harsh@example.com")
)
```

### Generic Models

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Response(BaseModel, Generic[T]):
    data: T
    status: int
    message: str

# Usage
response = Response[User](
    data=User(name="John", age=30, email="john@example.com"),
    status=200,
    message="Success"
)
```

---

## Model Configuration

Configure model behavior using `model_config`:

```python
from pydantic import ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,  # Strip whitespace from strings
        validate_assignment=True,    # Validate on attribute assignment
        frozen=True,                 # Make model immutable
        extra='forbid',              # Forbid extra attributes
        use_enum_values=True,        # Use enum values instead of enum objects
    )
    
    name: str
    age: int
```

**Common Configuration Options:**
- `str_strip_whitespace` - Auto-strip string whitespace
- `validate_assignment` - Validate when assigning to attributes
- `frozen` - Make instances immutable
- `extra='allow'|'forbid'|'ignore'` - Handle extra fields
- `populate_by_name` - Allow population by field name
- `from_attributes` - Enable ORM mode (from SQLAlchemy, etc.)

---

## Serialization

### Export to Dictionary

```python
user = User(name="John", age=30, email="john@example.com")

# Basic dict
user_dict = user.model_dump()

# Exclude fields
user_dict = user.model_dump(exclude={'email'})

# Include only specific fields
user_dict = user.model_dump(include={'name', 'age'})

# Exclude None values
user_dict = user.model_dump(exclude_none=True)
```

### Export to JSON

```python
# JSON string
json_str = user.model_dump_json()

# Pretty JSON
json_str = user.model_dump_json(indent=2)

# Exclude fields
json_str = user.model_dump_json(exclude={'email'})
```

### Parsing Data

```python
# From dictionary
user = User(**data_dict)
# or
user = User.model_validate(data_dict)

# From JSON
user = User.model_validate_json(json_string)
```

---

## Advanced Features

### Computed Fields

```python
from pydantic import computed_field

class Rectangle(BaseModel):
    width: float
    height: float

    @computed_field
    @property
    def area(self) -> float:
        return self.width * self.height

rect = Rectangle(width=10, height=5)
print(rect.area)  # 50.0
```

### Field Aliases

```python
class APIResponse(BaseModel):
    user_name: str = Field(alias='userName')
    user_email: str = Field(alias='userEmail')
    
    model_config = ConfigDict(populate_by_name=True)

# Can use either name
response = APIResponse(userName="John", userEmail="john@example.com")
# or
response = APIResponse(user_name="John", user_email="john@example.com")
```

### Private Attributes

```python
class User(BaseModel):
    name: str
    _internal_id: int = 0  # Private attribute

    def __init__(self, **data):
        super().__init__(**data)
        self._internal_id = id(self)
```

### Model Copy & Update

```python
user1 = User(name="John", age=30, email="john@example.com")

# Create copy with updates
user2 = user1.model_copy(update={'age': 31})

# Deep copy
user3 = user1.model_copy(deep=True)
```

### Custom Error Messages

```python
from pydantic import ValidationError

try:
    user = User(name="Jo", age=200, email="invalid")
except ValidationError as e:
    print(e.json())
    # Detailed error information
```

### Schema Generation

```python
# JSON Schema
schema = User.model_json_schema()

# OpenAPI compatible schema
from pydantic import Field

class Product(BaseModel):
    name: str = Field(..., description="Product name", examples=["Laptop"])
    price: float = Field(..., description="Price in USD", examples=[999.99])
```

---

## Best Practices

1. **Use `Annotated` for Field constraints** (Pydantic V2)
   ```python
   name: Annotated[str, Field(min_length=3)]
   ```

2. **Use `default_factory` for mutable defaults**
   ```python
   items: List[str] = Field(default_factory=list)
   ```

3. **Combine validators appropriately**
   - `@field_validator` for single field logic
   - `@model_validator(mode="before")` for preprocessing
   - `@model_validator(mode="after")` for cross-field validation

4. **Leverage type hints**
   - Use `Optional[T]` for nullable fields
   - Use `Union[T1, T2]` for multiple types
   - Use proper imports from `typing`

5. **Handle validation errors gracefully**
   ```python
   try:
       model = Model(**data)
   except ValidationError as e:
       handle_errors(e.errors())
   ```

6. **Use EmailStr, HttpUrl for specialized validation**

7. **Configure models for your use case**
   - Set appropriate `extra` policy
   - Enable `validate_assignment` if needed
   - Use `frozen=True` for immutable models

---

## Key Differences: Pydantic V1 vs V2

| Feature | V1 | V2 |
|---------|----|----|
| Validators | `@validator` | `@field_validator` |
| Root validators | `@root_validator` | `@model_validator` |
| Config | `class Config` | `model_config = ConfigDict()` |
| Field syntax | `Field(...)` | `Annotated[type, Field(...)]` |
| Export | `.dict()`, `.json()` | `.model_dump()`, `.model_dump_json()` |
| Parse | `.parse_obj()` | `.model_validate()` |
| Performance | Slower | ~5-50x faster (Rust core) |

---

## Resources

- **Official Docs**: [https://docs.pydantic.dev/](https://docs.pydantic.dev/)
- **GitHub**: [https://github.com/pydantic/pydantic](https://github.com/pydantic/pydantic)
- **Migration Guide**: [V1 to V2 Migration](https://docs.pydantic.dev/latest/migration/)

---

## License

This guide is for educational purposes. Pydantic is MIT licensed.
