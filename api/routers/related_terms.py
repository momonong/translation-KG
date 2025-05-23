import re
from fastapi import APIRouter, Query
from api.models.models import GroupedRelatedTermsResponse
from tools.graph_query import get_related_terms
from tools.load_graph import load_graph_from_jsonl

router = APIRouter()
G = load_graph_from_jsonl("data/graph_data.jsonl")


def detect_language_prefix(term: str) -> str:
    return "zh" if re.search(r"[\u4e00-\u9fff]", term) else "en"

@router.get("/related_terms", response_model=GroupedRelatedTermsResponse)
def get_related_terms_api(term: str = Query(...), top_k: int = 20):
    lang = detect_language_prefix(term)
    term_uri = f"/c/{lang}/{term.strip().lower()}"
    groups = get_related_terms(G, term_uri, top_k_per_relation=top_k)
    return {"term": term.strip(), "groups": groups}

