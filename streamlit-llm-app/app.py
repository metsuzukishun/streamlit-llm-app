##################################
# ライブラリのインポート
##################################
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

##################################
# LLMに問い合わせる関数の定義
##################################
def get_llm_response(user_input, expert_type):
    """
    user_input: 入力フォームからの文字列
    expert_type: ラジオボタンで選択された専門家の種類
    """
    # 専門家ごとのシステムメッセージ
    if expert_type == "A":  # ITエンジニア
        system_msg = "あなたはITエンジニアです。ユーザーの質問に技術的に正確に答えてください。"
    elif expert_type == "B":  # 栄養士
        system_msg = "あなたは栄養士です。ユーザーの質問に健康面から答えてください。"
    else:
        system_msg = "あなたは一般知識のあるアシスタントです。"

    # プロンプトテンプレート作成
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_msg),
        HumanMessagePromptTemplate.from_template("{user_input}")
    ])
    
    # LLMインスタンス作成
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
    
    # 実際にLLMに問い合わせ
    response = llm(prompt.format_prompt(user_input=user_input).to_messages())
    
    return response[0].content

##################################
# StreamlitでWeb画面作成
##################################
st.title("LLM質問アプリ")
st.write("このアプリでは、テキストを入力して専門家に質問できます。")
st.write("専門家の種類を選択してから質問してください。")

# 入力フォーム
user_input = st.text_input("質問を入力してください:")

# ラジオボタンで専門家選択
expert_type = st.radio("専門家を選択:", ["A", "B"])

# 送信ボタン
if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        answer = get_llm_response(user_input, expert_type)
        st.write("### 回答")
        st.write(answer)
