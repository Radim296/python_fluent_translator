from genericpath import isdir
import os
from typing import Optional

from pydantic import ValidationError

from src.schemas.dictionary import FluentDictionary


class TranslatorCache:
    __cache_folder_path: str

    def __init__(self) -> None:
        self.__cache_folder_path = f"{os.getcwd()}/.fluent_translator_cache/"
        self.__create_cache_folder()

    def __create_cache_folder(self) -> None:
        if not os.path.isdir(self.__cache_folder_path):
            os.mkdir(self.__cache_folder_path)

    def __get_dictionary_cache_path(self, language_code: str) -> str:
        return f"{self.__cache_folder_path}{language_code}.json"

    def set(self, dictionary: FluentDictionary) -> None:
        with open(
            self.__get_dictionary_cache_path(language_code=dictionary.language_code),
            "w",
        ) as file:
            file.write(dictionary.model_dump_json(indent=True))

    def delete(self, language_code: str) -> None:
        path: str = self.__get_dictionary_cache_path(language_code=language_code)

        if os.path.isfile(path):
            os.remove(path)
        else:
            raise ValueError(f"The dictionary by {language_code} does not exist")

    def get(self, language_code: str = "en") -> Optional[FluentDictionary]:
        path: str = self.__get_dictionary_cache_path(language_code=language_code)

        if os.path.isfile(path):
            with open(path) as file:
                try:
                    return FluentDictionary.model_validate_json(file.read())
                except ValidationError:
                    self.delete(language_code=language_code)
