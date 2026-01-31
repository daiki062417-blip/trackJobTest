#編集　久米田
#20250130/0201 TrackJor Hackthon
import streamlit as st
import pandas as pd
import os

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
    if st.button("タスク一覧"):
        navigate_to('task_list')
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
        task_name = st.text_input("タスク名")
        task_detail = st.text_area("タスクの詳細")
        task_date = st.text_area("タスクを行う時期・日時")
        task_assignee = st.text_input("引き継ぎ担当者")
        submitted = st.form_submit_button("提出")

        if submitted:
            data = pd.DataFrame(
                [[task_name, task_detail, task_date, task_assignee]], 
                columns=["タスク名", "タスクの詳細", "タスクを行う時期・日時", "引き継ぎ担当者"]
            )
            DATA_FILE = "tasks.csv"

            if not os.path.isfile(DATA_FILE):
                data.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
            else:
                data.to_csv(DATA_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')

            st.success("タスクが正常に保存されました")
            st.session_state.page = "main" # navigate_toの代わりに直接代入
            st.rerun()
    
#「タスク一覧」の画面
elif st.session_state.page == 'task_list':
    st.header("タスク一覧")
    st.write("引き継ぐ必要のあるタスクは下の通りです")
    
    # ホームに戻るボタン
    if st.button("ホームに戻る"):
        navigate_to('main')
        st.rerun()

    if os.path.isfile("tasks.csv"):
        df = pd.read_csv("tasks.csv")
        st.dataframe(df,use_container_width=True )
        st.info(f"現在、{len(df)}件のタスクが登録されています。")
    else:
        st.warming("まだ登録されたタスクはありません")

    
#「引き継ぎ希望申請」の画面




#『最適な引き継ぎ先の確認・情報リセット」の画面



