import requests
import json

API_URL = "https://libretranslate.com/translate"

def detect_language(text):
    return "zh" if any(ord(ch) > 128 for ch in text) else "en"

def translate(text):
    source = detect_language(text)
    target = "en" if source == "zh" else "zh"

    payload = {
        "q": text,
        "source": source,
        "target": target,
        "format": "text",
        "api_key": ""  # <= 關鍵在這一行
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()["translatedText"]
        print(f"\n{text} ➜ {result}")
        return result
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP error: {e}")
        print(f"🔍 Response: {response.text}")
    except Exception as e:
        print(f"❌ General error: {e}")


if __name__ == "__main__":
    # 你可以自由更換這些句子
    inputs = [
        "representation",
        "光流是什麼意思？",
        "I love neural rendering.",
        "這是一個用於機器翻譯的測試句子"
    ]

    for sentence in inputs:
        translate(sentence)
