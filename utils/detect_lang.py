import re

def detect_language_prefix(term: str) -> str:
    return "zh" if re.search(r"[\u4e00-\u9fff]", term) else "en"

