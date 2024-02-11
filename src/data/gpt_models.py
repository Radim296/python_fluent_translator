from dataclasses import dataclass
from typing import Dict


@dataclass
class GptModelData:
    price_per_1000_input_tokens: float
    price_per_1000_output_tokens: float
    temperature: float = 0.2
    max_tokens: int = 2000
    top_p: int = 1
    frequency_penalty: int = 0
    presence_penalty: int = 0


GPT_MODELS: Dict[str, GptModelData] = {
    "gpt-3.5-turbo": GptModelData(
        price_per_1000_input_tokens=0.0015, price_per_1000_output_tokens=0.002
    ),
    "gpt-3.5-turbo-16k": GptModelData(
        price_per_1000_input_tokens=0.003, price_per_1000_output_tokens=0.004
    ),
    "gpt-4": GptModelData(
        price_per_1000_input_tokens=0.03, price_per_1000_output_tokens=0.06
    ),
    "gpt-4-1106-preview": GptModelData(
        price_per_1000_input_tokens=0.01, price_per_1000_output_tokens=0.03
    ),
    "gpt-4-0125-preview": GptModelData(
        price_per_1000_input_tokens=0.01, price_per_1000_output_tokens=0.03
    ),
    "text-davinci-003": GptModelData(
        price_per_1000_input_tokens=0.02, price_per_1000_output_tokens=0.02
    ),
}
