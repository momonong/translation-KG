# api/main.py
from fastapi import FastAPI
from api.routers import keywords, related_terms
from fastapi.middleware.cors import CORSMiddleware
from api.cors import ExtensionCORS


app = FastAPI()


# ✅ 加入這段
app.add_middleware(
    ExtensionCORS,
    allow_origins=[],  # 初始為空，會動態加入來自 extension 的 origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(keywords.router, prefix="/api")
app.include_router(related_terms.router, prefix="/api")
