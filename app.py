import streamlit as st
import os
from dotenv import load_dotenv # 環境変数（OPENAI_API_KEYなど）を読み込むライブラリ
from langchain_openai import ChatOpenAI 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage

# 🚨 最重要: プロジェクトフォルダ直下の .env ファイルから環境変数を読み込む
load_dotenv() 

# --- 1. 専門家の定義とシステムメッセージ ---
PROFILES = {
    "ソフトウェアアーキテクト": (
        "あなたは20年の経験を持つ世界クラスのソフトウェアアーキテクトです。ユーザーの質問に対し、"
        "技術的な視点、システム設計、効率性、スケーラビリティに焦点を当てて、専門的かつ実践的なアドバイスを日本語で提供します。"
        "回答は簡潔かつ明確でなければなりません。"
    ),
    "歴史学者": (
        "あなたは世界史を専門とする有名な歴史学者です。ユーザーの質問に対し、"
        "特定の歴史的出来事の背景、文化的文脈、そして関連する人物の詳細な分析を、教育的で学術的なトーンで日本語で提供します。"
        "回答には必ず歴史的な年月日を含めてください。"
    ),
}

# --- 2. LLMからの回答を取得する関数 ---
# 「入力テキスト」と「ラジオボタンでの選択値」を引数として受け取り、LLMからの回答を戻り値として返します。
@st.cache_data
def generate_response(user_input: str, expert_name: str) -> str:
    """
    ユーザー入力と専門家の種類に基づいてLLMに問い合わせを行い、回答を返します。
    """
    
    # 環境変数にキーが存在するか確認
    if not os.environ.get("OPENAI_API_KEY"):
        return "エラー：OpenAI APIキーが環境変数に設定されていません。プロジェクト直下の `.env` ファイルを確認してください。"

    # 選択された専門家のシステムメッセージを取得
    system_message_content = PROFILES.get(expert_name)
    
    if not system_message_content:
        return "エラー：選択された専門家の設定が見つかりません。"

    # プロンプトテンプレートを作成
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_message_content),
        ("human", "{text}"),
    ])

    # モデルの初期化 (ChatOpenAIを使用)
    try:
        # load_dotenv() で読み込まれた環境変数から、ChatOpenAIがAPIキーを自動で取得します。
        llm = ChatOpenAI(
            model="gpt-4o-mini", 
            temperature=0.7
        ) 
    except Exception as e:
        # LLM初期化時の一般的なエラーメッセージ
        return f"LLMの初期化中にエラーが発生しました: {e}"


    # LangChainの処理パイプラインを構築: プロンプト -> LLM
    chain = prompt | llm

    # 処理を実行
    try:
        response = chain.invoke({"text": user_input})
        return response.content
    except Exception as e:
        # 通信エラーやその他の実行時エラー
        return f"LLMとの通信中にエラーが発生しました: {e}"


# --- 3. StreamlitアプリケーションのUI構築 ---

# タイトル
st.title("🤖 LLMペルソナ切り替えデモアプリ (Powered by OpenAI)")

# Webアプリの概要と操作方法の明示
st.markdown("""
このWebアプリは、ユーザーの質問に対して、LLM（OpenAI/ChatGPT）に特定の**専門家**として振る舞わせることで、回答のスタイルや内容を切り替えます。

### 🚀 操作方法
1.  **専門家を選択:** 下のラジオボタンで回答してほしい専門家を選んでください。
2.  **質問を入力:** 下のテキストエリアに質問を入力してください。
3.  **送信:** 「回答を生成」ボタンを押すと、選択した専門家の視点から回答が生成されます。
""")

# --- メインコンテンツ ---

# 専門家選択のラジオボタン
expert_options = list(PROFILES.keys())
selected_expert = st.radio(
    "1. 回答してほしい専門家を選んでください:",
    expert_options,
    index=0,
    horizontal=True,
)

# 入力フォーム
user_input = st.text_area(
    "2. 質問を入力してください（例：次の時代のITトレンドは？、日本の戦国時代の特徴は？）",
    height=150,
)

# 送信ボタン
if st.button("回答を生成", type="primary"):
    if user_input:
        # プログレスバー（ローディング表示）
        with st.spinner(f"「{selected_expert}」として回答を生成中です..."):
            # 関数を呼び出し、回答を取得
            response_text = generate_response(user_input, selected_expert)
            
            # 結果表示
            st.subheader(f"🗣️ {selected_expert} の回答")
            st.info(response_text)
    else:
        st.warning("質問を入力してからボタンを押してください。")


# --- 実行時の注意点 ---
st.caption("---")
st.caption("🔑 **APIキー設定の確認**: このアプリは、`python-dotenv`を使用し、`app.py`と同じ階層にある `.env` ファイルから `OPENAI_API_KEY` を読み込みます。")
st.caption("`.env` ファイルに `OPENAI_API_KEY=\"sk-あなたのキー\"` の形式で記述されていることをご確認ください。")