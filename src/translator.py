import asyncio
from collections import deque
import os
import time
from typing import Deque, Dict, List, Optional
from src.data.language_names import LANGUAGE_NAMES_BY_CODE


from src.schemas.config import TranslatorConfig
from src.schemas.dictionary import FluentDictionary
from src.utils.cache import TranslatorCache
from src.utils.gpt import GptTranslator
from src.utils.parser import FluentDictionaryParser


class FluentDictionaryTranslator:
    gpt_translator: GptTranslator
    fluent_parser: FluentDictionaryParser
    config: TranslatorConfig

    def __init__(self, config: TranslatorConfig) -> None:
        self.config = config
        self.gpt_translator = GptTranslator(config=config)
        self.fluent_parser = FluentDictionaryParser(config=config)

    def log(self, message: str) -> None:
        if self.config.logs:
            print(message)

    async def translate(self, language_code: str) -> None:
        main_dictionary: FluentDictionary = self.fluent_parser.parse_file(
            file_path=self.config.dictionaries["en"], language_code="en"
        )
        dictionary_to_translate: Optional[FluentDictionary] = None
        cached_main_dictionary: Optional[FluentDictionary] = None

        if os.path.isfile(self.config.dictionaries[language_code]):
            dictionary_to_translate = self.fluent_parser.parse_file(
                self.config.dictionaries[language_code], language_code=language_code
            )

        if self.config.use_cache:
            cached_main_dictionary = TranslatorCache().get()

        dictionary_values: Dict[str, str] = (
            main_dictionary.messages
            if dictionary_to_translate is None
            else dictionary_to_translate.messages
        )
        keys_to_translate: List[str] = self.fluent_parser.get_keys_to_translate(
            main_dictionary=main_dictionary,
            dictionary_to_translate=dictionary_to_translate,
            cached_main_dictionary=cached_main_dictionary,
        )

        translation_queue: Deque = deque(keys_to_translate)
        t1 = time.time()

        while translation_queue:
            keys: List[str] = []

            for _ in range(self.config.parrarel_keys_translation_limit):
                if translation_queue:
                    keys.append(translation_queue.popleft())

            translated_values: List[str] = await self.gpt_translator.translate_many(
                values=[main_dictionary.messages[key] for key in keys],
                target_language=LANGUAGE_NAMES_BY_CODE[language_code],
            )

            for i in range(len(translated_values)):
                dictionary_values[keys[i]] = translated_values[i].result()

            self.log(
                f"{language_code}: {100 - round(len(translation_queue)/len(keys_to_translate) * 100, 2)}%"
            )

        if dictionary_to_translate:
            dictionary_to_translate.messages = dictionary_values
        else:
            dictionary_to_translate = FluentDictionary(
                language_code=language_code,
                path=self.config.dictionaries[language_code],
                messages=translated_values,
            )

        dictionary_to_translate = self.fluent_parser.fix_dictionary_order(
            dictionary=dictionary_to_translate, main_dictionary=main_dictionary
        )

        self.fluent_parser.load_to_file(dictionary=dictionary_to_translate)

        self.log(f"{language_code}: {self.gpt_translator.get_usage_price()} USD")
        self.log(f"{language_code}: {time.time() - t1}")

    async def bulk_translate(self, language_codes: List[str]) -> None:
        language_codes_queue: Deque = deque(language_codes)

        while language_codes_queue:
            codes: List[str] = []

            for _ in range(self.config.bulk_parrarel_translation_limit):
                if language_codes_queue:
                    code: str = language_codes_queue.popleft()

                    if code != "en":
                        codes.append(code)

            async with asyncio.TaskGroup() as tg:
                for code in codes:
                    tg.create_task(self.translate(language_code=code))
