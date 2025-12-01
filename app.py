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
    
    # 役割に応じたシステムプロンプトの切り替え（専門領域の定義）
    if role_selection == "熟練のエンジニア":
        system_message = (
            "あなたは高度な技術知識を持つ熟練のITエンジニアです。"
            "ユーザーのアイデアや質問に対して、「技術的な実現可能性」「開発効率」「セキュリティ」「システム設計」"
            "の観点から専門的なアドバイスをしてください。"
            "精神論ではなく、具体的かつ論理的な技術論を中心に回答してください。"
        )
    else:  # 敏腕マーケター
        system_message = (
            "あなたは市場を知り尽くした敏腕マーケティングコンサルタントです。"
            "ユーザーのアイデアや質問に対して、「顧客ターゲット」「市場ニーズ」「収益化」「ブランディング」"
            "の観点から専門的なアドバイスをしてください。"
            "技術的な詳細よりも、ユーザーにどう届けるか、どう売るかを中心に回答してください。"
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
        temperature=0.7
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
同じ相談内容でも、**「技術的な視点」**と**「ビジネス的な視点」**では回答内容が大きく異なります。それぞれの専門家の意見を聞いてみましょう。

### 操作方法
1. 下のラジオボタンから、意見を聞きたい**専門家の種類**を選んでください。
2. テキストボックスに**相談したい内容**を入力してください。
3. **「回答をもらう」ボタン**を押すと、専門的見地からのアドバイスが表示されます。
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
    placeholder="例：新しいスマホアプリを作って一攫千金を狙いたいのですが、どう思いますか？"
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