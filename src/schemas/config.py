from typing import Dict, List
from pydantic import BaseModel


class TranslatorConfig(BaseModel):
    gpt_model: str = "gpt-3.5-turbo"
    logs: bool = True
    use_cache: bool = False # only updated items will be translated
    update_all: bool = True
    parrarel_keys_translation_limit: int = 1 # how may keys to translate at a time
    bulk_parrarel_translation_limit: int = 1 # how many dictionaries translate at a time
    ignored_keys: List[str] = [] # these keys would be kept in english
    translate_only: List[str] = [] # translate only these keys

    gpt_token: str = "sk-"
    dictionaries: Dict[str, str] = {
        "en": "en.ftl"
    }
