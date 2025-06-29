from fastapi import APIRouter, HTTPException, Query
from api.models.translate import TranslateResponse
from tools.translate import translate

router = APIRouter()

@router.get("/translate", response_model=TranslateResponse)
def translate_text(
    text: str = Query(..., description="Text to be translated"),
    target: str = Query(..., description="Target language, must be 'en' or 'zh'"),
    alternatives: int = Query(1, ge=1, le=5, description="Number of alternative translations (1-5)")
):
    # 檢查目標語言是否合法
    if target not in ("en", "zh"):
        raise HTTPException(status_code=400, detail=f"Invalid target language: {target}. Only 'en' and 'zh' are supported.")

    try:
        return translate(text, target=target, alt=alternatives)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
