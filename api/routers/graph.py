import re
from fastapi import APIRouter, Query, Request
from tools.graph_query import extract_subgraph_data

router = APIRouter()


def detect_language_prefix(term: str) -> str:
    return "zh" if re.search(r"[\u4e00-\u9fff]", term) else "en"


@router.get("/graph", response_model=list)
def get_related_terms_graph(
    request: Request,
    term: str = Query(...),
    top_k: int = 20,
):
    G = request.app.state.graph  # 透過全局 graph
    lang = detect_language_prefix(term)
    term_uri = f"/c/{lang}/{term.strip().lower()}"
    graph_data = extract_subgraph_data(G, term_uri, top_k_per_relation=top_k)
    return graph_data
