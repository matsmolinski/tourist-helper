from dataclasses import dataclass


@dataclass
class TranslationResponse:
    original_text: str
    translation_text: str
    image_url: str
