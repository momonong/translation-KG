from tools.parser import parse_sentence, extract_keywords
from tools.load_graph import load_graph_from_jsonl
from tools.graph_query import get_related_terms

jsonl_path = "data/graph_data.jsonl"
G = load_graph_from_jsonl(jsonl_path)

sentence = "This course if about knowledge graph."
tokens = parse_sentence(sentence)
keywords = extract_keywords(tokens)

print(f"\n原始句子：{sentence}")
print(f"擷取出的關鍵詞（建議查詢）：{keywords}\n")

test_term = f"/c/en/{keywords[0]}"
results = get_related_terms(G, test_term)

print(f"\n關鍵詞：{test_term}")
for source, rel, target in results:
    print(f"{source} --[{rel}]--> {target}")

print(f"\n總關聯數量：{len(results)}")