from typing import Dict, List, Optional

from src.data.const_values import COMMENT_KEY
from src.schemas.config import TranslatorConfig
from src.schemas.dictionary import FluentDictionary


class FluentDictionaryParser:
    config: TranslatorConfig

    def __init__(self, config: TranslatorConfig) -> None:
        self.config = config

    def parse_file(self, file_path: str, language_code: str) -> FluentDictionary:
        """
        The `parse_file` function reads a file and extracts key-value pairs, where the keys are lines that
        contain an equal sign and the values are the lines that follow.

        :param file_path: The `file_path` parameter is a string that represents the path to the file that
        needs to be parsed
        :type file_path: str
        :return: The function `parse_file` returns a dictionary (`Dict[str, str]`) containing key-value
        pairs parsed from the file specified by the `file_path` parameter.
        """
        result_dict: Dict[str, str] = {}
        with open(file_path, "r", encoding="utf-8") as file:
            lines: List[str] = file.readlines()
            key: Optional[str] = None
            value: str = ""

            for line in lines:
                if not line.lstrip().startswith("#"):
                    if "=" in line:
                        if key:
                            result_dict[key.strip(" ")] = value.rstrip("\n")
                        key, value = line.split("=", 1)
                    else:
                        value += line
                elif line.count("#") > 5:
                    result_dict[COMMENT_KEY] = line

            if key:
                result_dict[key.strip(" ")] = value.rstrip("\n")

        return FluentDictionary(
            language_code=language_code, path=file_path, messages=result_dict
        )

    def get_diff_keys(self, first_dictionary: FluentDictionary, second_dictionary: FluentDictionary) -> List[str]:
        keys: List[str] = []

        assert first_dictionary.language_code == second_dictionary.language_code

        for key, value in first_dictionary.messages.items():
            second_value: Optional[str] = second_dictionary.messages.get(key)

            if (not second_value) or (second_value != value):
                keys.append(key)

        return keys

    def get_keys_to_translate(
        self,
        main_dictionary: FluentDictionary,
        dictionary_to_translate: Optional[FluentDictionary] = None,
        cached_main_dictionary: Optional[FluentDictionary] = None
    ) -> List[str]:
        """
        The function `get_keys_to_translate` returns a list of keys from a FluentDictionary object that are
        not present in the config.

        :param dictionary: A FluentDictionary object that contains a collection of messages and their
        translations
        :type dictionary: FluentDictionary
        :return: a list of keys from the `dictionary` that are not present in `self.config`.
        """
        keys: List[str] = []

        if not self.config.translate_only:
            if not cached_main_dictionary:
                for key in main_dictionary.messages.keys():
                    if (key not in self.config.ignored_keys) and (key != COMMENT_KEY):
                        if self.config.update_all:
                            keys.append(key)
                        else:
                            if not dictionary_to_translate:
                                keys.append(key)
                            elif dictionary_to_translate.messages.get(key) is None:
                                keys.append(key)
            else:
                assert not self.config.translate_only, "You can't use cache with configured translate only items"
                assert self.config.update_all, "This value should be set to True"

                for key in self.get_diff_keys(first_dictionary=main_dictionary, second_dictionary=cached_main_dictionary):
                    if (key not in self.config.ignored_keys) and (key != COMMENT_KEY):
                        keys.append(key)
        else:
            for key in self.config.translate_only:
                assert main_dictionary.messages.get(key)
                keys.append(key)

        return keys

    def load_to_file(self, dictionary: FluentDictionary) -> None:
        """
        The function `load_to_file` writes the contents of a dictionary to a file, with special handling for
        multiline values.

        :param dictionary: The `dictionary` parameter is a dictionary that contains key-value pairs. The
        keys represent the names of the variables or settings, and the values represent their corresponding
        values
        :type dictionary: Dict[str, str]
        :param file_path: The `file_path` parameter is a string that represents the path to the file where
        the dictionary will be loaded. It should include the file name and extension. For example,
        `"data.txt"` or `"path/to/file/data.txt"`
        :type file_path: str
        """
        with open(dictionary.path, "w") as file:
            for key, value in dictionary.messages.items():
                key = key.strip(" ")
                if key == COMMENT_KEY:
                    print(f"\n{value}", file=file)
                else:
                    if value.count("\n") > 1:
                        print(f"{key} =", end="\n", file=file)
                        lines = value.split("\n")

                        while len(lines) > 0 and lines[0] == "":
                            lines.pop(0)

                        for i in range(len(lines)):
                            if lines[i] == "":
                                print(file=file)
                            else:
                                print(f"    {lines[i].lstrip()}", file=file)

                        print(file=file)
                    else:
                        print(f"{key} = {value.lstrip()}\n", file=file)
