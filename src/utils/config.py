import json
from src.data.const_values import CONFIG_FILENAME
from src.schemas.config import TranslatorConfig
from os.path import isfile


class ConfigReader:
    filename: str

    def __init__(self, config_filename: str = CONFIG_FILENAME) -> None:
        self.filename = config_filename

    def get_config(self) -> TranslatorConfig:
        if isfile(self.filename):
            with open(self.filename) as file:
                config: TranslatorConfig = TranslatorConfig.model_validate_json(json_data=file.read())
                return config
        else:
            with open(self.filename, "w") as file:
                file.write(TranslatorConfig().model_dump_json(indent=3))

            raise ValueError("Config file not found: created new")
