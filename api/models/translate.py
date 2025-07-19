from pydantic import BaseModel

class TranslateRequest(BaseModel):
    text: str
    context: str

class TranslateResponse(BaseModel):
    result: str  
