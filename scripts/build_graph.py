import csv
import json
import networkx as nx


def build_knowledge_graph(csv_path: str) -> nx.MultiDiGraph:
    G = nx.MultiDiGraph()

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=",")
        line_count = 0

        for row in reader:
            row = [cell.strip().strip('"') for cell in row]
            if len(row) != 5:
                continue
            _, rel, start, end, _ = row
            if not (start.startswith("/c/en/") or start.startswith("/c/zh/")):
                continue
            if not (end.startswith("/c/en/") or end.startswith("/c/zh/")):
                continue

            G.add_node(start)
            G.add_node(end)
            G.add_edge(start, end, key=rel, label=rel)
            line_count += 1

    print(f"共建立 {G.number_of_nodes()} 節點，{G.number_of_edges()} 邊")
    return G


def get_related_terms(graph: nx.MultiDiGraph, term: str):
    if term not in graph:
        return []

    related = []

    # 出邊（term → other）
    for nbr in graph[term]:
        for k in graph[term][nbr]:
            rel = graph[term][nbr][k].get("label", "")
            related.append((term, rel, nbr))

    # 入邊（other → term）
    for nbr in graph.predecessors(term):
        for k in graph[nbr][term]:
            rel = graph[nbr][term][k].get("label", "")
            related.append((nbr, rel, term))

    return related


if __name__ == "__main__":
    import os
    from tools.load_graph import load_graph_from_jsonl
    from tools.graph_query import get_related_terms

    # 替換為你的 CSV 檔案路徑
    csv_path = "data/conceptnet_filtered.csv"
    jsonl_path = "data/graph_data.jsonl"
    if not os.path.exists(jsonl_path):
        G = build_knowledge_graph(csv_path)
    else:
        G = load_graph_from_jsonl(jsonl_path)
    print(f"\n節點數：{G.number_of_nodes()}")
    print(f"邊數：{G.number_of_edges()}")

    sample_nodes = list(G.nodes)[:10]
    print("\n範例節點前 10 筆：")
    for node in sample_nodes:
        print(node)

    # 測試詞彙查詢
    test_term = "/c/en/course"
    results = get_related_terms(G, test_term)

    print(f"\n關鍵詞：{test_term}")
    for source, rel, target in results:
        print(f"{source} --[{rel}]--> {target}")

    print(f"\n總關聯數量：{len(results)}")
