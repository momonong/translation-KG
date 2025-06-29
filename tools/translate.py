import os
import requests
from utils.detect_lang import detect_language_prefix
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("TRANSLATE_API_URL")


def translate(text: str) -> dict:
    source = detect_language_prefix(text)
    target = "en" if source == "zh" else "zh"

    payload = {"q": text, "source": source, "target": target, "format": "text"}

    response = requests.post(API_URL, json=payload)
    response.raise_for_status()
    return {
        "original": text,
        "translated": response.json()["translatedText"],
        "source_lang": source,
        "target_lang": target,
    }
