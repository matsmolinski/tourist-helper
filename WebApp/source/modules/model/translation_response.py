from dataclasses import dataclass


@dataclass
class TranslationResponse:
    original_text: str
    translation_text: str
    image_url: str


@dataclass
class TranslationListEntry:
    timestamp: str
    status: str
    image_url: str
    token: str

