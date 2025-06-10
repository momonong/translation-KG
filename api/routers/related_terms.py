import re
from fastapi import APIRouter, Query, Request
from api.models.models import GroupedRelatedTermsResponse
from tools.graph_query import extract_subgraph_data

router = APIRouter()


def detect_language_prefix(term: str) -> str:
    return "zh" if re.search(r"[\u4e00-\u9fff]", term) else "en"


@router.get("/related_terms", response_model=GroupedRelatedTermsResponse)
def get_related_terms_api(request: Request, term: str = Query(...), top_k: int = 20):
    G = request.app.state.graph
    lang = detect_language_prefix(term)
    term_uri = f"/c/{lang}/{term.strip().lower()}"
    groups = extract_subgraph_data(G, term_uri, top_k_per_relation=top_k)
    return {"term": term.strip(), "groups": groups}
