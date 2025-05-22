import json
import networkx as nx


def export_graph_to_jsonl(graph: nx.MultiDiGraph, output_path: str):
    count = 0
    with open(output_path, "w", encoding="utf-8") as f:
        for u, v, k, data in graph.edges(keys=True, data=True):
            record = {
                "source": u,
                "target": v,
                "relation": data.get("label", k),
                "weight": data.get("weight", 1.0)  # 預設為 1.0，如果沒有設定
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1
    print(f"✅ 已輸出 {count} 筆關係到：{output_path}")


if __name__ == "__main__":
    from scripts.build_graph import build_knowledge_graph

    csv_path = "data/conceptnet_filtered.csv"
    output_path = "data/graph_data.jsonl"

    print("🚀 建立知識圖譜中...")
    G = build_knowledge_graph(csv_path)

    print("💾 輸出 JSONL...")
    export_graph_to_jsonl(G, output_path)
