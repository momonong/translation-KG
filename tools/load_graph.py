import json
import networkx as nx


def load_graph_from_jsonl(jsonl_path: str) -> nx.MultiDiGraph:
    G = nx.MultiDiGraph()

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            u = data["source"]
            v = data["target"]
            rel = data["relation"]
            weight = data.get("weight", 1.0)  # 預設 1.0，如未指定

            G.add_node(u)
            G.add_node(v)
            G.add_edge(u, v, key=rel, label=rel, weight=weight)

    print(f"✅ 已載入圖：{G.number_of_nodes()} 節點，{G.number_of_edges()} 邊")
    return G
