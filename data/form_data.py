from dataclasses import dataclass
from typing import Literal


@dataclass
class RegistrationFormData:
    full_name: str
    email: str
    age: int
    phone: str


@dataclass
class TableRow:
    row_id: str
    name: str
    email: str
    status: Literal["Active", "Inactive"]


@dataclass
class DragItem:
    label: str
    index: int


AsyncButtonState = Literal["default", "loading", "success", "error"]
