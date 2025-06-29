from fastapi import APIRouter, HTTPException
from api.models.translate import TranslateRequest, TranslateResponse
from tools.translate import translate


router = APIRouter()


@router.post("/translate", response_model=TranslateResponse)
def translate_text(req: TranslateRequest):
    try:
        return translate(req.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
