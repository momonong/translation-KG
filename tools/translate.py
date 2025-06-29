import os
import requests
from dotenv import load_dotenv
from utils.chinese_s2t import to_traditional, convert_list


load_dotenv()

API_URL = os.getenv("TRANSLATE_API_URL")
API_KEY = os.getenv("TRANSLATE_API_KEY", "")


def translate(text: str, target: str = "zh", alt: int = 3) -> dict:
    if target not in ("en", "zh"):
        raise ValueError(
            f"Unsupported target language: {target}. Only 'en' and 'zh' are supported."
        )

    payload = {
        "q": text,
        "source": "auto",
        "target": target,
        "format": "text",
        "alternatives": alt,
        "api_key": API_KEY,
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()

        translated = (
            to_traditional(data.get("translatedText", ""))
            if target == "zh"
            else data.get("translatedText", "")
        )
        alternatives = (
            convert_list(data.get("alternatives", []))
            if target == "zh"
            else data.get("alternatives", [])
        )

        return {
            "original": text,
            "translated": translated,
            "alternatives": alternatives,
            "source_lang": data.get("detectedLanguage", {}).get("language", "auto"),
            "target_lang": target,
        }

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"🔌 POST request failed: {e}")
    except (ValueError, KeyError, TypeError) as e:
        raise RuntimeError(f"🔍 Unexpected response format: {response.text}")
