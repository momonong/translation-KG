# api/main.py
from fastapi import FastAPI
from api.routers import keywords, related_terms
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^chrome-extension://.*$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(keywords.router, prefix="/api")
app.include_router(related_terms.router, prefix="/api")
