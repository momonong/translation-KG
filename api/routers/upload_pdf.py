# api/routers/upload_pdf.py
import os
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from tools.pdf_reader import save_and_return_pdf_id

PDF_FOLDER = os.getenv("PDF_FOLDER", "pdf_files")
os.makedirs(PDF_FOLDER, exist_ok=True)

router = APIRouter()

@router.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    pdf_id = save_and_return_pdf_id(file)
    # 這裡的路徑不用帶 prefix，FastAPI include_router 時自動補上
    pdf_url = f"/api/pdfview/{pdf_id}"
    return JSONResponse({"pdf_url": pdf_url})
