from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.models.translate import TranslateResponse
from tools.translate import translate

router = APIRouter()

class TranslateRequest(BaseModel):
    text: str
    context: str

@router.post("/translate", response_model=TranslateResponse)
def translate_text(payload: TranslateRequest):
    try:
        return translate(
            text=payload.text,
            context=payload.context
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
