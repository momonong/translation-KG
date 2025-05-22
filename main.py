from tools.parser import parse_text, extract_keywords
from tools.load_graph import load_graph_from_jsonl
from tools.graph_query import get_related_terms

jsonl_path = "data/graph_data.jsonl"
G = load_graph_from_jsonl(jsonl_path)

sentence = """Following recent developments in quantum machine learning techniques, several algorithms have been developed for disease detection. This study explored the application of a hybrid quantum-classical algorithm for classifying region-of-interest time-series data obtained from resting-state functional magnetic resonance imaging (fMRI) in patients with early-stage cognitive impairment. Classical one-dimensional convolutional layers were used in conjunction with quantum convolutional neural networks in our hybrid algorithm. In a classical simulation, the proposed hybrid algorithms in our study exhibited higher balanced accuracies than classical convolutional neural networks under similar training conditions. In addition, in our study, among the 116 brain regions, two brain regions (the right hippocampus and left parahippocampus) that showed relatively higher classification performance in the proposed algorithm were confirmed. The associations of the two selected regions with cognitive decline, as found in previous studies, were validated using seed-based functional connectivity analysis. Thus, we confirmed both improvement in model performance with the quantum convolutional neural network and neuroscientific validity of brain regions from our hybrid quantum-classical model."""
tokens = parse_text(sentence)
keywords = extract_keywords(tokens)

print(f"\n原始句子：{sentence}")
print(f"擷取出的關鍵詞（建議查詢）：{keywords}\n")

test_term = f"/c/en/{keywords[0]}"
results = get_related_terms(G, test_term, top_k_per_relation=20)

print(f"\n關鍵詞：{test_term}")
for source, rel, target, weight in results:
    print(f"{source} --[{rel} ({weight:.2f})]--> {target}")

print(f"\n總關聯數量：{len(results)}")