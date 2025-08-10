from pydantic import BaseModel
from typing import Optional, Literal

class TranslateRequest(BaseModel):
    text: str
    context: str
    pos_en: Optional[str] = None  # "noun" | "verb" | "adj" | "adv" | "phrase" | "unknown"
    pos_zh: Optional[str] = None


class TranslateResponse(BaseModel):
    result: str  
    normalized_target: Optional[str] = None
    normalized_pos: Optional[Literal["noun","verb","adj","adv","det","pron","num","phrase","unknown"]] = None