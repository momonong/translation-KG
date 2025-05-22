# api/main.py
from fastapi import FastAPI
from api.routers import keywords, related_terms

app = FastAPI()

app.include_router(keywords.router, prefix="/api")
app.include_router(related_terms.router, prefix="/api")
