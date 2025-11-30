import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

# ==========================================
# 1. 環境設定
# ==========================================
# ローカル開発用に.envファイルを読み込む（Streamlit CloudではSecretsが優先されます）
load_dotenv()

# ページ設定
st.set_page_config(page_title="専門家AIチャット", page_icon="🤖")

# ==========================================
# 2. 関数定義
# ==========================================
def get_llm_response(user_input, role_selection):
    """
    ユーザーの入力と選択された役割を受け取り、LLMの回答を返す関数
    
    Args:
        user_input (str): ユーザーからの質問テキスト
        role_selection (str): ラジオボタンで選択された役割の名称

    Returns:
        str: LLMからの回答テキスト
    """
    
    # 役割に応じたシステムプロンプトの切り替え
    if role_selection == "熱血！スポーツインストラクター":
        system_message = (
            "あなたは超ポジティブで熱血なスポーツインストラクターです。"
            "「ナイスファイト！」「君ならできる！」などの言葉を多用し、"
            "ユーザーを全力で励ましながら、勢いよく回答してください。"
            "文末には必ず「🔥」をつけてください。"
        )
    else:  # 冷徹な論理学者
        system_message = (
            "あなたは感情を持たない冷徹な論理学者です。"
            "客観的な事実と論理のみに基づいて、簡潔に回答してください。"
            "感情的な言葉や挨拶は一切省いてください。"
            "文末には必ず「(論理的帰結)」をつけてください。"
        )

    # プロンプトテンプレートの作成
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "{text}")
    ])

    # モデルの準備 (Streamlit CloudのSecretsからAPIキーを読み込む前提)
    # ※APIキーのエラーハンドリング
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return "エラー: OpenAI APIキーが設定されていません。Streamlit CloudのSecretsを設定してください。"

    llm = ChatOpenAI(
        api_key=api_key,
        model="gpt-3.5-turbo",
        temperature=0.7
    )

    # Chainの構築 (LCEL記法: Prompt -> LLM -> OutputParser)
    chain = prompt | llm | StrOutputParser()

    # Chainの実行
    response = chain.invoke({"text": user_input})
    
    return response

# ==========================================
# 3. UI（画面表示）部分
# ==========================================

# タイトルとアプリ概要の表示
st.title("🤖 性格が変わる！AI専門家チャット")
st.markdown("""
### アプリの概要
このアプリでは、選択した「専門家（人格）」に合わせて、AIが回答してくれます。
同じ質問でも、選ぶ相手によって全く違う返答が返ってくる様子を楽しんでください。

### 操作方法
1. 下のラジオボタンから、相談したい**専門家の種類**を選んでください。
2. テキストボックスに**質問や相談**を入力してください。
3. **「回答をもらう」ボタン**を押すと、AIからの返事が表示されます。
""")

st.divider() # 区切り線

# ラジオボタン（専門家の選択）
role_options = ["熱血！スポーツインストラクター", "冷徹な論理学者"]
selected_role = st.radio(
    "誰に相談しますか？",
    role_options,
    index=0
)

# テキスト入力フォーム
user_text = st.text_input(
    "質問を入力してください",
    placeholder="例：最近やる気が出ないんだけど、どうしたらいい？"
)

# 送信ボタンと回答表示
if st.button("回答をもらう"):
    if user_text:
        # 処理中はスピナー（ぐるぐる）を表示
        with st.spinner("AIが回答を生成中..."):
            # 定義した関数を呼び出して回答を取得
            answer = get_llm_response(user_text, selected_role)
            
        # 結果の表示
        st.markdown(f"### 【{selected_role}】からの回答")
        st.write(answer)
    else:
        st.warning("テキストを入力してください！")