import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from utils.detect_lang import detect_lang

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
    lang = detect_lang(context)
    if lang == "en":
        # 英文查詞 > 中文
        prompt = f"""
            請根據下列英文句子的語境，將指定單字「{word}」翻譯為台灣常用的繁體中文詞語，**嚴禁使用中國大陸詞彙**。
            請直接輸出下列 HTML 格式（**每一行都要有**），**不要補充說明，不要包 div/pre/code，只能回傳以下內容：**

            <b>查詢單字：</b>{word}<br>
            <b>主要義項：</b>（最適合此語境的台灣用語，單詞即可）<br>
            <b>詞性：</b>（如：名詞/動詞/形容詞…）<br>
            <b>語意說明：</b>（20字內簡明描述，請描述語境中的意思）<br>
            <b>其他常見義項：</b>
            <ul>
            <li>義項1（如有）</li>
            <li>義項2（如有）</li>
            </ul>

            英文句子：{context}
            查詢單字：{word}
        """

    elif lang == "zh":
        # 中文查詞 > 英文
        prompt = f"""
            請根據下列**中文句子**的語境，將指定單字「{word}」翻譯為**最貼切自然的英文詞彙**，請參考語境判斷詞義。
            請直接輸出下列 HTML 格式（每一行都要有），**不要補充說明，不要包 div/pre/code，只能回傳以下內容：**

            <b>查詢單字：</b>{word}<br>
            <b>主要義項：</b>（最貼切自然的英文單字）<br>
            <b>詞性：</b>（英文，例：noun/verb/adj...）<br>
            <b>語意說明：</b>（用英文，20 words 以內簡明描述，請描述語境中的意思）<br>
            <b>其他常見義項：</b>
            <ul>
            <li>義項1（如有，英文）</li>
            <li>義項2（如有，英文）</li>
            </ul>

            中文句子：{context}
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
