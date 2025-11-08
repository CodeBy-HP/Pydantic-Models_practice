## 🧩 Fields

Fields add **constraints**, **validation rules**, **metadata**, and **documentation** to individual model attributes.

### Common Parameters
| Parameter | Meaning | Example |
|------------|----------|----------|
| `...` | Required field (no default) | `name: str = Field(...)` |
| `gt`, `lt`, `ge`, `le` | Greater than / less than constraints | `price: float = Field(gt=0, lt=10000)` |
| `min_length`, `max_length` | Length constraints for strings/lists | `code: str = Field(min_length=3, max_length=10)` |
| `regex` | Regular expression pattern | `email: str = Field(regex=r"^\\S+@\\S+$")` |
| `description`, `example` | Metadata for documentation (e.g., FastAPI) | `Field(..., description="Product name")` |
| `default_factory` | Dynamic default value (e.g., list, dict) | `Field(default_factory=list)` |
| `title` | Field label or title | `Field(..., title="Username")` |
| `alias` | Alternate key name | `Field(..., alias="user_name")` |

### Example
```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(..., description="Product name")
    price: float = Field(gt=0, lt=10000, description="Price must be positive")
```

Using Annotated(just for cleaner syntax)
```python
from pydantic import BaseModel, Field
from typing import Annotated

class Product(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=50)]
    price: Annotated[float, Field(gt=0, lt=10000)]
```


🧩 5️⃣ Nested Models (Pydantic v2)
🟢 What It Means

You can use one Pydantic model inside another — just like nesting objects in JSON.
This allows structured, validated, and typed data hierarchies.

⚙️ Basic Example
from pydantic import BaseModel
from typing import Annotated
from pydantic import Field

class Address(BaseModel):
    city: Annotated[str, Field(min_length=2)]
    zip: Annotated[str, Field(min_length=5, max_length=10)]

class User(BaseModel):
    name: Annotated[str, Field(min_length=2)]
    address: Address


✅ Here:

The User model contains another model Address.

When a User instance is created, Pydantic automatically validates that:

address is a valid Address object.

The nested Address fields (city, zip) follow their constraints.

💡 Example Input (Dict form)
data = {
    "name": "Harsh",
    "address": {
        "city": "Ahmedabad",
        "zip": "380001"
    }
}

user = User(**data)
print(user)


✅ Output:

name='Harsh' address=Address(city='Ahmedabad', zip='380001')

🔍 Automatic Nested Validation

If you pass invalid nested data, Pydantic will show structured errors.

Example:

bad_data = {
    "name": "H",
    "address": {
        "city": "A",
        "zip": 123   # not string
    }
}

User(**bad_data)


❌ Raises a ValidationError like:

3 validation errors for User
name
  String should have at least 2 characters [type=string_too_short]
address.city
  String should have at least 2 characters [type=string_too_short]
address.zip
  Input should be a valid string [type=string_type]


🧠 Notice how Pydantic automatically points to nested paths like address.city.

🧱 Nested Lists or Dicts of Models

You can also nest lists or dictionaries of models.

class Address(BaseModel):
    city: str
    zip: str

class User(BaseModel):
    name: str
    addresses: list[Address]


✅ Example:

u = User(
    name="Alice",
    addresses=[
        {"city": "Surat", "zip": "395001"},
        {"city": "Vadodara", "zip": "390001"}
    ]
)


Pydantic automatically:

Converts dicts → Address objects

Validates all addresses

🧮 Nested Access

Once validated, you can easily access nested data:

print(u.addresses[0].city)  # Surat

🧰 Dict & JSON Conversion (Nested)

When you call .dict() or .model_dump():

print(u.model_dump())


You get:

{
    'name': 'Alice',
    'addresses': [
        {'city': 'Surat', 'zip': '395001'},
        {'city': 'Vadodara', 'zip': '390001'}
    ]
}


So the nesting structure remains consistent in both directions (input & output).

🧠 When It’s Used in FastAPI

Nested models appear in:

Complex request bodies:

{
    "user": {
        "name": "Alice",
        "address": {"city": "Delhi", "zip": "110001"}
    }
}


Database relationships (e.g., User → multiple Orders)

API responses (e.g., return object with nested details)

💡 Bonus: Optional Nested Models
class User(BaseModel):
    name: str
    address: Address | None = None  # or Optional[Address]


✅ This allows the address field to be missing or null.

⚙️ Summary (Pydantic v2 Nested Models)
Feature	Example	Behavior
Nested model field	address: Address	Validates sub-model
Nested lists	addresses: list[Address]	Validates each element
Nested dicts	contacts: dict[str, Contact]	Validates dict values
Optional nested	`address: Address	None`
Validation	Recursive	Errors show full path
Serialization	.model_dump()	Returns nested dict


🧩 6️⃣ Lists, Dicts, Optional, and Union in Pydantic v2

These come from the standard Python typing module, and Pydantic enhances them by:

validating the structure,

enforcing element types,

and automatically converting compatible inputs.

🟢 1. List — for arrays or multiple values
✅ Example
from pydantic import BaseModel
from typing import Annotated, List
from pydantic import Field

class User(BaseModel):
    tags: Annotated[List[str], Field(min_length=1)]

🧠 Notes

List[str] means: every element must be a string.

Field(min_length=1) means: at least one item required.

⚙️ Example Usage
User(tags=["python", "fastapi"])
# ✅ OK

User(tags=[])  
# ❌ ValidationError: list too short

⚡ Auto-conversion

Pydantic can auto-convert:

User(tags="python")  # ❌ not valid — must be list, not str
User(tags=("a", "b"))  # ✅ converted tuple → list

🟢 2. Dict — for key-value structures
✅ Example
from typing import Dict, Union

class User(BaseModel):
    preferences: Dict[str, Union[str, int]]

🧠 Notes

The key type must be a string.

The value can be either a str or an int because of the Union.

⚙️ Example
u = User(preferences={"theme": "dark", "font_size": 14})
print(u)
# ✅ preferences={'theme': 'dark', 'font_size': 14}

⚠️ Invalid Example
User(preferences={1: "dark"})
# ❌ keys must be strings

🟢 3. Optional — for nullable or missing fields
✅ Example
from typing import Optional

class User(BaseModel):
    phone: Optional[str] = None

🧠 Meaning

Optional[str] = value can be str or None.

If omitted, it will default to None unless another default is given.

⚙️ Example
User(phone="12345")  # ✅
User()               # ✅ phone=None
User(phone=None)     # ✅

🟢 4. Union — when multiple types are valid
✅ Example
from typing import Union

class Item(BaseModel):
    price: Union[int, float]

🧠 Meaning

Value can be either int or float.

Pydantic checks in order: tries int, then float.

⚙️ Example
Item(price=10)     # ✅ int
Item(price=10.5)   # ✅ float
Item(price="10")   # ✅ converted to int
Item(price="abc")  # ❌ invalid

🟣 Combining All Together
from typing import List, Dict, Optional, Union
from pydantic import BaseModel, Field
from typing import Annotated

class User(BaseModel):
    name: Annotated[str, Field(min_length=2)]
    tags: Annotated[List[str], Field(min_length=1)]
    preferences: Dict[str, Union[str, int]]
    phone: Optional[str] = None


✅ Example usage:

u = User(
    name="Harsh",
    tags=["dev", "ai"],
    preferences={"theme": "dark", "level": 3}
)
print(u.model_dump())


Output:

{
  'name': 'Harsh',
  'tags': ['dev', 'ai'],
  'preferences': {'theme': 'dark', 'level': 3},
  'phone': None
}

🧠 Bonus — Validation for Lists and Dicts

You can apply constraints to collection lengths:

class Product(BaseModel):
    tags: Annotated[List[str], Field(min_length=1, max_length=5)]
    metadata: Annotated[Dict[str, str], Field(min_length=1)]

⚙️ Summary Table
Type	Meaning	Example	Notes
List[T]	list of items of type T	List[str]	Validates each element
Dict[K, V]	key-value pairs	Dict[str, int]	Validates keys & values
Optional[T]	can be T or None	Optional[str]	Default = None if missing
Union[T1, T2]	either type allowed	Union[int, float]	Validates in declared order