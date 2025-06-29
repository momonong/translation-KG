from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import keywords, related_terms, graph, translate
from tools.load_graph import load_graph_from_jsonl

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^chrome-extension://.*$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.graph = load_graph_from_jsonl("data/graph_data.jsonl")

# Knowledge Graph API
app.include_router(keywords.router, prefix="/api")
app.include_router(related_terms.router, prefix="/api")
app.include_router(graph.router, prefix="/api")  

# Translation API
app.include_router(translate.router, prefix="/api")