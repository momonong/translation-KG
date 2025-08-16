import html
import os
import json
import re
from typing import Optional, Dict, Any, List, Tuple

from dotenv import load_dotenv
from google import genai
from google.genai import types
from utils.detect_lang import detect_lang

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 要求模型回 JSON
GEN_CONFIG_JSON = types.GenerateContentConfig(
    response_mime_type="application/json"
)

# ---------- 小工具 ----------
def _clean_list(items: Optional[List[str]]) -> List[str]:
    if not items:
        return []
    cleaned = []
    for s in items:
        if not s:
            continue
        t = str(s).strip()
        if not t:
            continue
        if re.fullmatch(r"(?:N/?A|n/a|none|\(if any\)|（?若有）?)", t, flags=re.I):
            continue
        cleaned.append(t)
    return cleaned

def _to_html_en2zh(data: Dict[str, Any]) -> str:
    if data.get("not_found"):
        return "無此單字"
    cm = html.escape(str(data.get("context_meaning", "")))
    exp = html.escape(str(data.get("meaning_explanation", "")))
    others = _clean_list(data.get("other_meanings", []))
    parts = [
        "<b style='font-weight:bold'>情境語意：</b>" + cm + "<br>",
        "<b style='font-weight:bold'>語意說明：</b>" + exp + "<br>",
        "<b style='font-weight:bold'>其他可能語意：</b>",
        "<ul>",
    ]
    for o in others:
        parts.append(f"<li>{html.escape(o)}</li>")
    parts.append("</ul>")
    return "".join(parts)

def _to_html_zh2en(data: Dict[str, Any]) -> str:
    if data.get("not_found"):
        return "無此單字"
    cm = html.escape(str(data.get("context_meaning", "")))
    exp = html.escape(str(data.get("meaning_explanation", "")))
    others = _clean_list(data.get("other_meanings", []))
    parts = [
        "<b style='font-weight:bold'>Contextual meaning:</b> " + cm + "<br>",
        "<b style='font-weight:bold'>Meaning description:</b> " + exp + "<br>",
        "<b style='font-weight:bold'>Other possible meanings:</b>",
        "<ul>",
    ]
    for o in others:
        parts.append(f"<li>{html.escape(o)}</li>")
    parts.append("</ul>")
    return "".join(parts)

# ---------- Prompts：加入 full_query（擴張片語）＋ pos ----------
_POS_ENUM = ["noun","verb","adj","adv","phrase","det","pron","num","unknown"]

def _prompt_en2zh(context: str, selection: str, pos_en: Optional[str]) -> str:
    pos_hint = (pos_en or "").strip().lower() or "unknown"
    return f"""
You are a careful EN→ZH(TW) lexicographer. Read the sentence and the user selection.
If the selection is part of a larger meaningful phrase (e.g., "no longer", "take off"), expand it.

Return **JSON only** with ALL keys below:

{{
  "not_found": false,                   // true if target not in sentence
  "full_query": "string",               // the most semantically complete span in the sentence that should be looked up (expanded from selection if needed)
  "pos": "one of {_POS_ENUM}",          // POS of full_query; "phrase" allowed
  "context_meaning": "string",          // best Taiwanese term (prefer single word)
  "meaning_explanation": "string",      // ≤20 Chinese characters
  "other_meanings": ["string"]          // other common TW options; [] if none
}}

Rules:
- Use **Taiwanese Traditional Chinese** only; avoid Mainland terms.
- If unsure about expansion, keep the selection as full_query and set pos="unknown".
- Do not add placeholders like "N/A".
- The selection is: "{selection}"
- POS hint (optional): {pos_hint}

Sentence:
{context}
""".strip()

def _prompt_zh2en(context: str, selection: str, pos_zh: Optional[str]) -> str:
    pos_hint = (pos_zh or "").strip().lower() or "unknown"
    return f"""
You are a precise ZH→EN lexicographer. Read the sentence and the user selection.
If the selection is part of a larger meaningful phrase, expand it.

Return **JSON only** with ALL keys below:

{{
  "not_found": false,                   // true if target not in sentence
  "full_query": "string",               // expanded phrase if needed
  "pos": "one of {_POS_ENUM}",
  "context_meaning": "string",          // best single English word if possible, or fixed phrase
  "meaning_explanation": "string",      // ≤20 words, brief gloss in English
  "other_meanings": ["string"]
}}

Rules:
- JSON only, no extra text.
- If unsure about expansion, keep the selection as full_query and set pos="unknown".
- Do not output placeholders like "N/A".
- The selection is: "{selection}"
- POS hint (optional): {pos_hint}

Chinese sentence:
{context}
""".strip()

def _parse_json(text: str) -> Dict[str, Any]:
    try:
        data = json.loads(text or "{}")
        if not isinstance(data, dict):
            return {}
        data.setdefault("not_found", False)
        data.setdefault("full_query", "")
        data.setdefault("pos", "unknown")
        data.setdefault("context_meaning", "")
        data.setdefault("meaning_explanation", "")
        data.setdefault("other_meanings", [])
        return data
    except Exception:
        return {}

# ---------- 主要函式：回 HTML ＋ 正規化資訊 ----------
def translate_with_llm(
    word: str,
    context: str,
    pos_en: Optional[str]=None,
    pos_zh: Optional[str]=None
) -> Dict[str, Any]:
    """
    回傳：
    {
      "html": "<b>…</b>…",          # 固定版型 HTML（不含查詢目標一行）
      "normalized_target": "not any longer",
      "normalized_pos": "adv"
    }
    """
    # 安全（只進 prompt，不直接渲染）
    selection_safe = html.escape(word)
    context_safe = html.escape(context)

    lang = detect_lang(context)

    if lang == "en":
        prompt = _prompt_en2zh(context=context_safe, selection=selection_safe, pos_en=pos_en)
        resp = client.models.generate_content(
            model="gemini-2.5-flash-lite-preview-06-17",
            contents=prompt,
            config=GEN_CONFIG_JSON,
        )
        data = _parse_json(getattr(resp, "text", "") or "")
        html_out = _to_html_en2zh(data)

    elif lang == "zh":
        prompt = _prompt_zh2en(context=context_safe, selection=selection_safe, po_zh=pos_zh)
        resp = client.models.generate_content(
            model="gemini-2.5-flash-lite-preview-06-17",
            contents=prompt,
            config=GEN_CONFIG_JSON,
        )
        data = _parse_json(getattr(resp, "text", "") or "")
        html_out = _to_html_zh2en(data)

    else:
        # 非英/中語句
        return {"html": "無此單字", "normalized_target": word, "normalized_pos": "unknown"}

    # 兜底：如果模型沒給 full_query，就用原 selection
    full_query = (data.get("full_query") or "").strip() or word
    pos = (data.get("pos") or "unknown").lower()
    if pos not in _POS_ENUM:
        pos = "unknown"

    # 如果 not_found，就保持原選字
    if data.get("not_found") is True:
        full_query = word
        pos = "unknown"

    return {
        "html": html_out,
        "normalized_target": full_query,
        "normalized_pos": pos
    }


# ==== 簡易測試 ====
if __name__ == "__main__":
    tests = [
        ("They do not work for us any longer.", "longer"),
        ("Ian is not an engineer any more.", "not"),
        ("They will no longer be enemies.", "no"),
        ("I quickly set the tent up and slept.", "up"),
    ]
    for s, w in tests:
        out = translate_with_llm(w, s)
        print(s)
        print("→", w, "=>", out["normalized_target"], "/", out["normalized_pos"])
        print(out["html"][:120], "...\n")
