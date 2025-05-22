# api/main.py
from fastapi import FastAPI
from api.routers import keywords, related_terms
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


# ✅ 加入這段
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "chrome-extension://kmbpineinpkiobkfoggcaabgonkknnjj"
    ],  # 你的 Extension ID
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(keywords.router, prefix="/api")
app.include_router(related_terms.router, prefix="/api")
