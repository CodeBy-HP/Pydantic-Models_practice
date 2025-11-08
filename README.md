## 🧩 Fields

Fields add **constraints**, **validation rules**, **metadata**, and **documentation** to individual model attributes.

### Common Parameters
| Parameter | Meaning | Example |
|------------|----------|----------|
| `...` | Required field (no default) | `name: str = Field(...)` |
| `gt`, `lt`, `ge`, `le` | Greater than / less than constraints | `price: float = Field(gt=0, lt=10000)` |
| `min_length`, `max_length` | Length constraints for strings/lists | `code: str = Field(min_length=3, max_length=10)` |
| `regex` | Regular expression pattern | `email: str = Field(regex=r"^\S+@\S+$")` |
| `description`, `example` | Metadata for docs (e.g., FastAPI) | `Field(..., description="Product name")` |

### Example
```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(..., description="Product name")
    price: float = Field(gt=0, lt=10000, description="Price must be positive")
