import spacy

# 載入英文 NLP 模型
nlp = spacy.load("en_core_web_sm")


# tools/parser.py
MAX_LENGTH = 2000  # 可依實際需求調整


def parse_text(text: str):
    """
    處理文字斷詞與語法分析，並限制輸入長度
    """
    if len(text) > MAX_LENGTH:
        raise ValueError(f"輸入長度過長，最多允許 {MAX_LENGTH} 個字元")

    doc = nlp(text)
    tokens = []
    for token in doc:
        if not token.is_space:
            tokens.append(
                {
                    "text": token.text,
                    "lemma": token.lemma_,
                    "pos": token.pos_,
                    "tag": token.tag_,
                    "dep": token.dep_,
                    "head": token.head.text,
                }
            )
    return tokens


def extract_keywords(tokens, allowed_pos={"NOUN", "VERB", "ADJ"}):
    """
    從解析結果中擷取關鍵詞（根型 lemma）
    """
    keywords = []
    for t in tokens:
        if t["pos"] in allowed_pos and t["lemma"].isalpha():
            keywords.append(t["lemma"].lower())
    return list(set(keywords))  # 去除重複


if __name__ == "__main__":
    text = """Following recent developments in quantum machine learning techniques, several algorithms have been developed for disease detection. This study explored the application of a hybrid quantum-classical algorithm for classifying region-of-interest time-series data obtained from resting-state functional magnetic resonance imaging (fMRI) in patients with early-stage cognitive impairment. Classical one-dimensional convolutional layers were used in conjunction with quantum convolutional neural networks in our hybrid algorithm. In a classical simulation, the proposed hybrid algorithms in our study exhibited higher balanced accuracies than classical convolutional neural networks under similar training conditions. In addition, in our study, among the 116 brain regions, two brain regions (the right hippocampus and left parahippocampus) that showed relatively higher classification performance in the proposed algorithm were confirmed. The associations of the two selected regions with cognitive decline, as found in previous studies, were validated using seed-based functional connectivity analysis. Thus, we confirmed both improvement in model performance with the quantum convolutional neural network and neuroscientific validity of brain regions from our hybrid quantum-classical model."""

    results = parse_text(text)

    print(f"\n🔍 原始文本：{text}\n")
    print("解析結果：")
    print(f"{'Token':<15}{'Lemma':<15}{'POS':<8}{'Dep':<15}{'Head'}")
    print("-" * 60)
    for token in results:
        print(
            f"{token['text']:<15}{token['lemma']:<15}{token['pos']:<8}{token['dep']:<15}{token['head']}"
        )

    keywords = extract_keywords(results)
    print(f"\n🔑 擷取出的關鍵詞（建議查詢）：{keywords}")
