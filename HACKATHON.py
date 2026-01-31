#編集　久米田
#20250130/0201 TrackJor Hackthon
import streamlit as st

#最初の画面
st.title("引き継ぎ管理アプリ")

if 'page' not in st.session_state:
    st.session_state.page='main'

def navigate_to(page_name):
    st.session_state.page = page_name

#ホーム画面の作成
if st.session_state.page == 'main':
    st.header("引き継ぎ管理アプリ")
    st.write("自分が行いたい業務を選んでください")
    if st.button("タスク入力"):
        navigate_to('task_input')
    if st.button("引き継ぎ希望申請"):
        navigate_to('application')
    if st.button('結果の確認・情報リセット'):
        navigate_to('results and reset ')

#「タスク入力」の画面
elif st.session_state.page == 'task_input':
    st.header("タスク入力")
    st.write("引き継ぎたいタスクを入力してください")
    
    # フォーム外のボタン
    if st.button("ホームに戻る"):
        navigate_to('main')
        st.rerun() # 画面を即座に切り替えるために追加
    
    # フォームの開始
    with st.form(key='task_form'):
        st.text_input("タスク名")
        st.text_area("タスクの詳細")
        st.text_area("タスクを行う時期・日時")
        st.text_input("引き継ぎ担当者")
        submitted = st.form_submit_button("提出")
        if submitted:
            st.session_state.page = "main" # navigate_toの代わりに直接代入
            st.rerun()
    
#「引き継ぎ希望申請」の画面


#『結果の確認・情報リセット」の画面

#テスト_春日井

