from typing import Dict
from pydantic import BaseModel


class FluentDictionary(BaseModel):
    language_code: str
    path: str
    messages: Dict[str, str]
