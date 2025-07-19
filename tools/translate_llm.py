import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Google Search (grounding) tool
grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

def translate_with_llm(word, context):
    """
    使用 gemini-2.5-flash-lite-preview-06-17 + Google Search Tool 做 context-aware 查詞
    必要時自動查網路資訊
    """
    prompt = f"""
    請根據下列英文句子的語境，將指定單字「{word}」翻譯為台灣常用繁體中文，嚴禁使用中國大陸詞彙。
    請直接輸出下方 HTML 格式，並務必每一行、每個部份都照下面範例格式產生：

    <b>查詢單字：</b>{word}<br>
    <b>主要義項：</b>…<br>
    <b>詞性：</b>…<br>
    <b>語意說明：</b>…<br>
    <b>其他常見義項：</b>
    <ul>
    <li>義項1</li>
    <li>義項2</li>
    </ul>

    不要補充說明，不要包其他 div 或 pre 或 code block，只能回傳上述內容。

    英文句子：{context}
    查詢單字：{word}
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite-preview-06-17",
        contents=prompt,
        config=config,
    )
    # print(f"LLM 回應：{response.text.strip()}")
    return response.text.strip()

# ==== 測試範例 ====
if __name__ == "__main__":
    test_cases = [
        (
            "April is the cruellest month, breeding / Lilacs out of the dead land, mixing / Memory and desire, stirring / Dull roots with spring rain.",
            "stirring"
        ),
        (
            "She felt herself transfixed by the beam of the lighthouse, unable to move, as though under a spell.",
            "beam"
        ),
        (
            "I am silver and exact. I have no preconceptions. Whatever I see I swallow immediately / Just as it is, unmisted by love or dislike.",
            "swallow"
        ),
        (
            "Give every man thy ear, but few thy voice; Take each man's censure, but reserve thy judgment.",
            "censure"
        ),
        (
            "The narrative unfolds with a haunting stillness, every movement weighted with meaning.",
            "stillness"
        ),
        (
            "He smiled understandingly—much more than understandingly. It was one of those rare smiles with a quality of eternal reassurance in it.",
            "reassurance"
        ),
        (
            "Hope is the thing with feathers / That perches in the soul— / And sings the tune without the words— / And never stops—at all—",
            "perches"
        ),
    ]


    for idx, (sentence, word) in enumerate(test_cases, 1):
        print(f"--- 文學範例 {idx} ---")
        print("原文句子：", sentence)
        output = translate_with_llm(word, sentence)
        print("查詞結果：\n" + output)
        print("\n")
