import streamlit as st


st.set_page_config(page_title="引き継ぎ管理アプリ", page_icon="📝")


st.markdown("""
    <style>
    /* 全体の背景色 */
    .stApp {
        background-color: #fdfdfd;
    }
    /* ボタンのデザインを可愛く */
    div.stButton > button {
        border-radius: 12px;
        border: 2px solid #6cace4;
        background-color: white;
        color: #6cace4;
        font-weight: bold;
        transition: 0.2s;
        padding: 0.5rem 1rem;
    }
    div.stButton > button:hover {
        background-color: #6cace4;
        color: white;
    }
    /* 入力フォームの枠を強調 */
    .stForm {
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)


if 'page' not in st.session_state:
    st.session_state.page = 'main'

def navigate_to(page_name):
    st.session_state.page = page_name

# --- ホーム画面の作成 ---
if st.session_state.page == 'main':
    st.title("✨ 引き継ぎ管理アプリ ✨")
    st.write("自分が行いたい業務を選んでください")
    st.divider() 

    # 元のボタン名をすべて維持
    if st.button("📥 タスク入力"):
        navigate_to('task_input')
    if st.button("🙋 引き継ぎ希望申請"):
        navigate_to('application')
    if st.button('🧹 結果の確認・情報リセット'):
        navigate_to('results_reset')

# --- 「タスク入力」の画面 ---
elif st.session_state.page == 'task_input':
    st.title("📥 タスク入力")
    st.write("引き継ぎたいタスクを入力してください")
    
    # フォーム外のボタン
    if st.button("🏠 ホームに戻る"):
        navigate_to('main')
        st.rerun() 
    
    # フォームの開始
    with st.form(key='task_form'):
        st.text_input("📋 タスク名", placeholder="例：議事録の作成")
        st.text_area("📝 タスクの詳細")
        st.text_input("📅 タスクを行う時期・日時") 
        st.text_input("👤 引き継ぎ担当者")
        
        submitted = st.form_submit_button("提出")
        if submitted:
            st.balloons()
            st.session_state.page = "main"
            st.rerun()

# --- 「引き継ぎ希望申請」の画面
elif st.session_state.page == 'application':
    st.title("🙋 引き継ぎ希望申請")
    if st.button("ホームに戻る"):
        navigate_to('main')
        st.rerun()

# --- 「結果の確認・情報リセット」の画面
elif st.session_state.page == 'results_reset':
    st.title("🧹 結果の確認・情報リセット")
    if st.button("ホームに戻る"):
        navigate_to('main')
        st.rerun()