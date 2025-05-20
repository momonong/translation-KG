# parser/parser.py
import spacy

# 載入英文 NLP 模型
nlp = spacy.load("en_core_web_sm")


def parse_sentence(text: str):
    """
    將句子斷詞並輸出基本詞性、語意資訊
    """
    doc = nlp(text)
    tokens = []

    for token in doc:
        if not token.is_space:  # 跳過空白符號
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
    從解析結果中擷取重要詞彙（根型 lemma）
    """
    keywords = []
    for t in tokens:
        if t["pos"] in allowed_pos and t["lemma"].isalpha():
            keywords.append(t["lemma"].lower())
    return list(set(keywords))  # 去除重複


if __name__ == "__main__":
    sentence = "Freedom is a basic human right."
    results = parse_sentence(sentence)

    print(f"\n🔍 原始句子：{sentence}\n")
    print("解析結果：")
    print(f"{'Token':<15}{'Lemma':<15}{'POS':<8}{'Dep':<15}{'Head'}")
    print("-" * 60)
    for token in results:
        print(
            f"{token['text']:<15}{token['lemma']:<15}{token['pos']:<8}{token['dep']:<15}{token['head']}"
        )

    # 擷取關鍵詞
    keywords = extract_keywords(results)
    print(f"\n🔑 擷取出的關鍵詞（建議查詢）：{keywords}")

