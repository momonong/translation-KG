import networkx as nx


def get_related_terms(graph: nx.MultiDiGraph, term: str):
    if term not in graph:
        return []
    related = []
    for nbr in graph[term]:
        for k in graph[term][nbr]:
            rel = graph[term][nbr][k].get("label", "")
            related.append((term, rel, nbr))
    for nbr in graph.predecessors(term):
        for k in graph[nbr][term]:
            rel = graph[nbr][term][k].get("label", "")
            related.append((nbr, rel, term))
    return related