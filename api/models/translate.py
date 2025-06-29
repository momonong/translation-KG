from pydantic import BaseModel

class TranslateRequest(BaseModel):
    text: str
    alternatives: int

class TranslateResponse(BaseModel):
    original: str
    translated: str
    alternatives: list[str] = []
    source_lang: str
    target_lang: str
