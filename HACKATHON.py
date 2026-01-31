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
