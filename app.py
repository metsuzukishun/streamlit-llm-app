import streamlit as st
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# 🚨 .env から環境変数を読み込む
load_dotenv()

# --- 1. 専門家定義 ---
PROFILES = {
    "ソフトウェアアーキテクト": (
        "あなたは20年の経験を持つ世界クラスのソフトウェアアーキテクトです。"
        "ユーザーの質問に対し、技術的な視点、システム設計、効率性、スケーラビリティに焦点を当てて、専門的かつ実践的に回答してください。"
        "回答は簡潔かつ明確にしてください。"
    ),
    "歴史学者": (
        "あなたは世界史の専門家です。ユーザーの質問に対し、歴史的出来事の背景、文化的文脈、関連人物の詳細分析を提供してください。"
        "回答には必ず年月日を含め、教育的・学術的なトーンで日本語で答えてください。"
    ),
}

# --- 2. 回答生成関数 ---
@st.cache_data(show_spinner=False)
def generate_response(user_input: str, expert_name: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "エラー：OpenAI APIキーが設定されていません。Streamlit Secrets または .env を確認してください。"

    # 専門家メッセージ
    system_msg = PROFILES.get(expert_name)
    if not system_msg:
        return "エラー：選択された専門家の設定が存在しません。"

    # プロンプト作成
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_msg),
        HumanMessagePromptTemplate.from_template("{text}")
    ])

    # ChatOpenAIモデルの初期化
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7, openai_api_key=api_key)

    # プロンプトにユーザー入力を適用
    messages = prompt.format_messages(text=user_input)

    try:
        response = llm(messages)
        return response.content
    except Exception as e:
        return f"LLM処理中にエラーが発生しました: {e}"

# --- 3. Streamlit UI ---
st.set_page_config(page_title="🤖 LLMペルソナ切り替えデモ", page_icon="🤖", layout="wide")
st.title("🤖 LLMペルソナ切り替えデモアプリ")

st.markdown("""
このWebアプリでは、LLMに特定の**専門家**として振る舞わせることで、回答スタイルを切り替えます。

### 操作方法
1. 専門家を選択
2. 質問を入力
3. 「回答を生成」を押す
""")

# 専門家選択
selected_expert = st.radio("回答してほしい専門家を選択:", list(PROFILES.keys()), index=0, horizontal=True)

# 質問入力
user_input = st.text_area("質問を入力してください:", height=150)

# 回答生成ボタン
if st.button("回答を生成"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner(f"{selected_expert}として回答を生成中..."):
            response = generate_response(user_input, selected_expert)
            st.subheader(f"🗣️ {selected_expert} の回答")
            st.info(response)

st.caption("---")
st.caption("🔑 **APIキーの確認**: Streamlit Secrets または .env に `OPENAI_API_KEY` を設定してください。")
