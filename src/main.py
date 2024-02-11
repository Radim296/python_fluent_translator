import argparse
import asyncio
from dataclasses import dataclass
from typing import Dict, Optional
import sys

from src.translator import FluentDictionaryTranslator
from src.utils import config


@dataclass
class TranslatorArgs:
    language_code: Optional[str] = None
    translate_all: bool = False


def parse_args() -> TranslatorArgs:
    assert len(sys.argv) in [2, 3]

    language_code: Optional[str] = None
    translate_all: bool = False

    if sys.argv[1] == "-a":
        translate_all = True
    elif sys.argv[1] == "-c":
        assert len(sys.argv) == 3
        language_code = sys.argv[2]

    return TranslatorArgs(language_code=language_code, translate_all=translate_all)



async def run_translator() -> None:
    translator = FluentDictionaryTranslator(config=config.ConfigReader().get_config())

    args = parse_args()

    if args.translate_all:
        await translator.bulk_translate(language_codes=list(translator.config.dictionaries.keys()))
    else:
        await translator.translate(language_code=args.language_code)

def main() -> None:
    asyncio.run(run_translator())

if __name__ == "__main__":
    main()
