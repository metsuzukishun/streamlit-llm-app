import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

# ==========================================
# 1. 環境設定
# ==========================================
# ローカル開発用に.envファイルを読み込む
load_dotenv()

# ページ設定
st.set_page_config(page_title="専門家AIアドバイザー", page_icon="👔")

# ==========================================
# 2. 関数定義
# ==========================================
def get_llm_response(user_input, role_selection):
    """
    ユーザーの入力と選択された役割を受け取り、その領域の専門家としての回答を返す関数
    
    Args:
        user_input (str): ユーザーからの質問テキスト
        role_selection (str): ラジオボタンで選択された役割の名称

    Returns:
        str: LLMからの回答テキスト
    """
    
    # 役割に応じたシステムプロンプトの切り替え
    # 【修正ポイント】専門外の質問には回答しないよう、強い制約を追加しました。
    if role_selection == "熟練のエンジニア":
        system_message = (
            "あなたは高度な技術知識を持つ熟練のITエンジニアです。"
            "ユーザーの質問に対して、「技術的な実現可能性」「開発効率」「セキュリティ」「システム設計」"
            "の観点から専門的なアドバイスをしてください。"
            "\n\n"
            "【重要：回答の制約】"
            "あなたはあくまで「技術」の専門家です。マーケティング、集客、売上向上、経営戦略などの"
            "「ビジネス・マーケティング領域」の質問には絶対に回答しないでください。"
            "もし専門外の質問が来た場合は、「申し訳ありません。私はエンジニアですので、マーケティングやビジネス戦略については専門外です。技術的な実装や設計についてであればお答えできます。」"
            "と明確に断ってください。"
        )
    else:  # 敏腕マーケター
        system_message = (
            "あなたは市場を知り尽くした敏腕マーケティングコンサルタントです。"
            "ユーザーの質問に対して、「顧客ターゲット」「市場ニーズ」「収益化」「ブランディング」"
            "の観点から専門的なアドバイスをしてください。"
            "\n\n"
            "【重要：回答の制約】"
            "あなたはあくまで「ビジネス」の専門家です。プログラミングコードの実装、サーバー構築、技術選定などの"
            "「システム開発・技術領域」の質問には絶対に回答しないでください。"
            "もし専門外の質問が来た場合は、「申し訳ありません。私はマーケターですので、技術的な実装やプログラミングについては専門外です。市場戦略や売れる仕組み作りについてであればお答えできます。」"
            "と明確に断ってください。"
        )

    # プロンプトテンプレートの作成
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "{text}")
    ])

    # モデルの準備
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return "エラー: OpenAI APIキーが設定されていません。Streamlit CloudのSecretsを設定してください。"

    llm = ChatOpenAI(
        api_key=api_key,
        model="gpt-3.5-turbo",
        temperature=0.5 # 役割を厳格に守らせるため、少し温度を下げました
    )

    # Chainの構築
    chain = prompt | llm | StrOutputParser()

    # Chainの実行
    response = chain.invoke({"text": user_input})
    
    return response

# ==========================================
# 3. UI（画面表示）部分
# ==========================================

# タイトルとアプリ概要の表示
st.title("👔 専門家AIアドバイザー")
st.markdown("""
### アプリの概要
このアプリでは、あなたの質問やアイデアに対して、異なる領域の専門家（AI）がアドバイスを提供します。
ただし、**彼らは自分の専門外のことには答えてくれません**。適切な相手を選んで相談してください。

### 操作方法
1. 下のラジオボタンから、意見を聞きたい**専門家の種類**を選んでください。
2. テキストボックスに**相談したい内容**を入力してください。
3. **「回答をもらう」ボタン**を押すと、専門的見地からのアドバイス（またはお断り）が表示されます。
""")

st.divider() # 区切り線

# ラジオボタン（専門家の選択）
role_options = ["熟練のエンジニア", "敏腕マーケター"]
selected_role = st.radio(
    "どの専門家に相談しますか？",
    role_options,
    index=0
)

# テキスト入力フォーム
user_text = st.text_input(
    "相談内容を入力してください",
    placeholder="例：アプリのサーバー構成はどうすべき？ / アプリの集客はどうすべき？"
)

# 送信ボタンと回答表示
if st.button("回答をもらう"):
    if user_text:
        # 処理中はスピナーを表示
        with st.spinner(f"{selected_role}が思考中..."):
            # 定義した関数を呼び出して回答を取得
            answer = get_llm_response(user_text, selected_role)
            
        # 結果の表示
        st.markdown(f"### 【{selected_role}】の見解")
        st.write(answer)
    else:
        st.warning("相談内容を入力してください！")