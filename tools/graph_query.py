import networkx as nx
from collections import defaultdict


def get_related_terms(graph: nx.MultiDiGraph, term: str, top_k_per_relation: int = 20):
    if term not in graph:
        return []

    grouped = defaultdict(list)

    # 出邊
    for nbr in graph[term]:
        for k in graph[term][nbr]:
            edge_data = graph[term][nbr][k]
            rel = edge_data.get("label", "")
            weight = edge_data.get("weight", 1.0)
            grouped[rel].append((term, rel, nbr, weight))

    # 入邊
    for nbr in graph.predecessors(term):
        for k in graph[nbr][term]:
            edge_data = graph[nbr][term][k]
            rel = edge_data.get("label", "")
            weight = edge_data.get("weight", 1.0)
            grouped[rel].append((nbr, rel, term, weight))

    # 每種關係取前 N 筆（依照 weight 排序）
    results = []
    for rel, edges in grouped.items():
        sorted_edges = sorted(edges, key=lambda x: -x[3])
        results.extend(sorted_edges[:top_k_per_relation])

    return results
