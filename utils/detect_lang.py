import re

def detect_language_prefix(term: str) -> str:
    if re.search(r"[\u4e00-\u9fff]", term):
        return "zh"
    elif re.search(r"[a-zA-Z]", term):
        return "en"
    else:
        return "unsupported"



if __name__ == "__main__":
    # 測試語言檢測
    test_terms = [
        "Hello, how are you?",
        "你好，你好吗？",
        "Bonjour, comment ça va?",
        "こんにちは、お元気ですか？"
    ]

    for term in test_terms:
        lang_prefix = detect_language_prefix(term)
        print(f"Term: {term} | Detected Language Prefix: {lang_prefix}")

    print(detect_language_prefix("你好"))        # zh
    print(detect_language_prefix("hello world")) # en
    print(detect_language_prefix("bonjour"))     # unsupported
    print(detect_language_prefix("123456"))      # unsupported
