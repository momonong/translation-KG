import json
import networkx as nx


def load_graph_from_jsonl(jsonl_path: str) -> nx.MultiDiGraph:
    G = nx.MultiDiGraph()

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            try:
                data = json.loads(line)
                u = data["source"]
                v = data["target"]
                rel = data["relation"]
                G.add_node(u)
                G.add_node(v)
                G.add_edge(u, v, key=rel, label=rel)
            except json.JSONDecodeError as e:
                print(f"❌ JSONDecodeError on line {i+1}: {e}")
                print("↪ line content:", line[:200])
                break  # 先抓出問題行
    return G


if __name__ == "__main__":
    jsonl_path = "data/graph_data.jsonl"
    G = load_graph_from_jsonl(jsonl_path)
    print(f"✅ 已載入圖：{G.number_of_nodes()} 節點，{G.number_of_edges()} 邊")
