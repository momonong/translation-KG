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
        prompt = f"""
            Based on the following English sentence, translate the specified word (“{word}”) into the most appropriate Taiwanese traditional Chinese word, strictly avoiding Mainland Chinese expressions.
            If the word does not exist in the sentence, simply output "無此單字" (do not speculate or invent any meaning).
            Please output the result using **only** the following HTML format, with every line included. 
            **Each <b> tag must have inline style: <b style="font-weight:bold">.**
            Do not add explanations, do not wrap in div/pre/code, and return only the following content:

            <b style="font-weight:bold">查詢單字：</b>{word}<br>
            <b style="font-weight:bold">主要義項：</b>(The most suitable Taiwanese word for this context, single word only)<br>
            <b style="font-weight:bold">詞性：</b>(e.g., 名詞/動詞/形容詞…)<br>
            <b style="font-weight:bold">語意說明：</b>(Within 20 characters, briefly describe the contextual meaning)<br>
            <b style="font-weight:bold">其他常見義項：</b>
            <ul>
            <li>義項1 (if any)</li>
            <li>義項2 (if any)</li>
            <li>義項3 (if any)</li>
            <li>義項4 (if any)</li>
            <li>義項5 (if any)</li>
            </ul>

            English sentence: {context}
            查詢單字：{word}
        """
    elif lang == "zh":
        prompt = f"""
            Based on the following Chinese sentence, translate the specified word (“{word}”) into the most natural and contextually appropriate English word.
            If the word does not exist in the sentence, simply output "無此單字" (do not speculate or invent any meaning).
            Please output the result using **only** the following HTML format, with every line included. 
            **Each <b> tag must have inline style: <b style="font-weight:bold">.**
            Do not add explanations, do not wrap in div/pre/code, and return only the following content:

            <b style="font-weight:bold">查詢單字：</b>{word}<br>
            <b style="font-weight:bold">主要義項：</b>(The most natural English word for this context, single word only)<br>
            <b style="font-weight:bold">詞性：</b>(English, e.g., noun/verb/adj...)<br>
            <b style="font-weight:bold">語意說明：</b>(In English, within 20 words, briefly describe the contextual meaning)<br>
            <b style="font-weight:bold">其他常見義項：</b>
            <ul>
            <li>Alternative 1 (if any, English)</li>
            <li>Alternative 2 (if any, English)</li>
            <li>Alternative 3 (if any, English)</li>
            <li>Alternative 4 (if any, English)</li>
            <li>Alternative 5 (if any, English)</li>
            </ul>

            Chinese sentence: {context}
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
