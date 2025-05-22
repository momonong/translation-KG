import networkx as nx
from collections import defaultdict

# 排序關係的優先順序（仿 ConceptNet 頁面呈現順序）
RELATION_PRIORITY = {
    "Synonym": 0,
    "FormOf": 1,
    "DerivedFrom": 2,
    "EtymologicallyRelatedTo": 3,
    "IsA": 4,
    "UsedFor": 5,
    "CapableOf": 6,
    "HasContext": 7,
    "RelatedTo": 8
}

def simplify_uri(uri: str) -> str:
    parts = uri.split("/")
    return parts[3] if len(parts) > 3 else uri

def simplify_relation(relation: str) -> str:
    return relation.replace("/r/", "")

def get_related_terms(graph: nx.MultiDiGraph, term: str, top_k_per_relation: int = 20):
    if term not in graph:
        return []

    grouped = defaultdict(list)

    # 出邊
    for nbr in graph[term]:
        for k in graph[term][nbr]:
            edge_data = graph[term][nbr][k]
            rel = simplify_relation(edge_data.get("label", ""))
            weight = edge_data.get("weight", 1.0)
            grouped[rel].append({
                "source": simplify_uri(term),
                "target": simplify_uri(nbr),
                "weight": weight
            })

    # 入邊
    for nbr in graph.predecessors(term):
        for k in graph[nbr][term]:
            edge_data = graph[nbr][term][k]
            rel = simplify_relation(edge_data.get("label", ""))
            weight = edge_data.get("weight", 1.0)
            grouped[rel].append({
                "source": simplify_uri(nbr),
                "target": simplify_uri(term),
                "weight": weight
            })

    # 每種關係取前 N 筆並排序
    results = []
    for rel, edges in grouped.items():
        sorted_edges = sorted(edges, key=lambda x: -x["weight"])
        results.append({
            "relation": rel,
            "items": sorted_edges[:top_k_per_relation]
        })

    # 根據優先順序排序（其餘未列在 RELATION_PRIORITY 的放在最後）
    results.sort(key=lambda x: RELATION_PRIORITY.get(x["relation"], 999))
    return results

# 測試用 CLI
if __name__ == "__main__":
    from tools.load_graph import load_graph_from_jsonl
    import json

    jsonl_path = "data/graph_data.jsonl"
    G = load_graph_from_jsonl(jsonl_path)

    term = "/c/en/graph"
    result = get_related_terms(G, term, top_k_per_relation=5)

    print(f"\n🔍 Term: {term}")
    print(json.dumps(result, indent=2, ensure_ascii=False))
