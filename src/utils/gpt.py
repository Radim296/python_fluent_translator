import asyncio
from typing import List

import openai
from src.data.gpt_models import GPT_MODELS, GptModelData

from src.schemas.config import TranslatorConfig

class GptTranslator:
    client: openai.AsyncClient
    config: TranslatorConfig
    input_tokens: int = 0
    output_tokens: int = 0
    target_language: str
    model_data: GptModelData

    def __init__(self, config: TranslatorConfig) -> None:
        self.client = openai.AsyncClient(api_key=config.gpt_token)
        self.config = config
        self.model_data = GPT_MODELS[self.config.gpt_model]

    async def translate(self, text: str, target_language: str) -> str:
        """
        The `translate` function takes a target language and a text as input, and uses OpenAI's chat
        completions API to generate a translated version of the text in the specified language. The
        translated text is then returned as the output of the function.

        :param target_language: The `target_language` parameter is a string that represents the language to
        which the `text` should be translated. It specifies the language code or name of the target
        language. For example, "en" for English, "es" for Spanish, "fr" for French, etc
        :type target_language: str
        :param text: The `text` parameter is the text that you want to translate to the target language
        :type text: str
        :return: The `translate` method returns the translated text as a string.
        """
        completition: openai.types.Completion = await self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You application localization helper from English to {target_language}"
                        "Do not write any comments, just translated text"
                        f"The translation should be correct and sound native for {target_language}"
                        "Be careful with the syntax"
                    ),
                },
                {
                    "role": "user",
                    "content": f"{text}",
                },
            ],
            model=self.config.gpt_model,
            temperature=self.model_data.temperature,
            top_p=self.model_data.top_p,
            presence_penalty=self.model_data.presence_penalty,
            frequency_penalty=self.model_data.frequency_penalty,
        )

        self.input_tokens += completition.usage.prompt_tokens
        self.output_tokens += completition.usage.completion_tokens

        return completition.choices[0].message.content

    async def translate_many(self, values: List[str], target_language: str) -> List[str]:
        """
        The function `translate_many` takes a list of strings as input and returns a list of translated
        strings using the `translate` function.

        :param values: A list of strings that need to be translated
        :type values: List[str]
        :return: a list of responses.
        """
        async with asyncio.TaskGroup() as tg:
            responses = [tg.create_task(self.translate(value, target_language=target_language)) for value in values]
        return responses

    def get_usage_price(self) -> float:
        """
        The function calculates the usage price based on the number of input and output tokens.
        :return: The method `get_usage_price` is returning a float value, which is the total usage price
        calculated based on the number of input tokens and output tokens.
        """
        return (
            self.input_tokens * self.model_data.price_per_1000_input_tokens / 1000
            + self.output_tokens * self.model_data.price_per_1000_output_tokens / 1000
        )
