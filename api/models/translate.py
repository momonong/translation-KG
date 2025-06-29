from pydantic import BaseModel


class TranslateRequest(BaseModel):
    text: str


class TranslateResponse(BaseModel):
    original: str
    translated: str
    source_lang: str
    target_lang: str
