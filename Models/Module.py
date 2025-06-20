from typing import List, Optional, Any
from pydantic import BaseModel
from datetime import datetime

class TableHeader(BaseModel):
    label: str
    headers: Optional[Any] = None
    cell_type: Optional[str] = None
    required: Optional[bool] = None
    allowed_values: Optional[Any] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    default_value: Optional[Any] = None
    min_width: Optional[float] = None
    max_width: Optional[float] = None
    help_text: Optional[str] = None

class TableRow(BaseModel):
    name: str
    required: Optional[bool] = None
    allowed_values: Optional[Any] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    default_value: Optional[Any] = None
    help_text: Optional[str] = None

class TableMetadata(BaseModel):
    headers: Optional[List[TableHeader]] = None
    rows: Optional[List[TableRow]] = None
    cell_type: Optional[str] = None
    min_col_width: Optional[float] = None
    max_col_width: Optional[float] = None
    horizontal_scroll_threshold: Optional[float] = None

class Question(BaseModel):
    question_id: str
    question: str
    type: str
    has_string_value: bool
    has_decimal_value: bool
    has_boolean_value: bool
    has_link: bool
    has_note: bool
    string_value_required: bool
    decimal_value_required: bool
    boolean_value_required: bool
    link_required: bool
    note_required: bool
    table_metadata: Optional[TableMetadata] = None

class QuestionCategory(BaseModel):
    id: str
    category_name: str
    questions: List[Question]

class Submodule(BaseModel):
    id: str
    submodule_name: str
    question_categories: List[QuestionCategory]

class Module(BaseModel):
    id: str
    company_id: str
    plant_id: str
    financial_year: str
    module_name: str
    submodules: List[Submodule]
    created_at: datetime
    updated_at: datetime
    # MongoDB _id is optional for Pydantic model use
    _id: Optional[str] = None
