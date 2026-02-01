import streamlit as st
import pandas as pd
import os

# 1. ページの設定
st.set_page_config(page_title="引き継ぎ管理アプリ", page_icon="📝")

# 2. デザイン（CSS）
st.markdown("""
    <style>
    .stApp { background-color: #fdfdfd; }
    
    div.stButton > button {
        border-radius: 12px;
        border: 2px solid #6cace4;
        background-color: white;
        color: #6cace4;
        font-weight: bold;
        transition: 0.2s;
        width: 100%;
        margin-bottom: 10px;
        min-height: 50px;
        font-size: 16px;
    }
    div.stButton > button:hover {
        background-color: #6cace4;
        color: white;
    }
    .stForm {
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 20px;
    }
            
    /*タイトルのレスポンシブ対応*/
    h1 {
            font-size: clamp(1.5rem, 5vw, 2.5rem);
            }


    /*テーブルのレスポンシブ対応*/
    [data-testid="stDataFrame"] {
        overflow-x: auto;
    }
            
    /* モバイル対応（画面幅768px以下） */
    @media (max-width: 768px) {
        .stApp {
            padding: 10px;
        }
            
        div.stButton > button {
            font-size: 14px;
            padding: 12px;
            min-height: 48px;
        }
            
        .stForm {
            padding: 15px;
            margin: 10px 0;
        }
            
    /*入力フィールドのフォントサイズ*/
    input, textarea {
        font-size: 16px !important;
    }
    
    /*データフレームのフォントサイズ*/
    [data-testid="stDataFrame"] {
            font-size: 12px;
        }
    }
            
    /* 小型モバイル対応（画面幅480px以下） */
    @media (max-width: 480px) {
            h1 {
                font-size: 1.5rem;
            }

            .stForm {
                padding: 10px;
            }

            div.stButton > button {
                font-size: 13px;
                min-height: 44px;
            }
    }
            
    /* タブレット横向き対応（画面幅769px〜1024px） */
    @media (min-width: 769px) and (max-width: 1024px) {
        .stApp {
            max-width: 900px;
            margin: 0 auto;
        }
    }

    </style>
    """, unsafe_allow_html=True)

# 3. 状態管理とナビゲーション
if 'page' not in st.session_state:
    st.session_state.page = 'main'

def navigate_to(page_name):
    st.session_state.page = page_name

# --- ホーム画面 ---
if st.session_state.page == 'main':
    st.title("✨ 引き継ぎ管理アプリ ✨")
    st.write("自分が行いたい業務を選んでください")
    st.divider() 

    
    if st.button("📥 タスク入力"):
        navigate_to('task_input')
    if st.button("📋 タスク一覧"):
        navigate_to('task_list')
    if st.button("🙋 引き継ぎ希望申請"):
        navigate_to('application')
    if st.button('🧹 結果の確認・情報リセット'):
        navigate_to('results_reset')

# --- 「タスク入力」画面 ---
elif st.session_state.page == 'task_input':
    st.title("📥 タスク入力")
    
    if st.button("🏠 ホームに戻る"):
        navigate_to('main')
        st.rerun() 
    
    with st.form(key='task_form'):
        # 重複していた入力フィールドを統合
        task_name = st.text_input("📋 タスク名", placeholder="例：議事録の作成")
        task_detail = st.text_area("📝 タスクの詳細")
        task_date = st.text_input("📅 タスクを行う時期・日時") 
        task_assignee = st.text_input("👤 引き継ぎ担当者")
        
        submitted = st.form_submit_button("提出")

        if submitted:
            # 1. まずデータを保存する
            data = pd.DataFrame(
                [[task_name, task_detail, task_date, task_assignee]], 
                columns=["タスク名", "タスクの詳細", "タスクを行う時期・日時", "引き継ぎ担当者"]
            )
            DATA_FILE = "tasks.csv"

            if not os.path.isfile(DATA_FILE):
                data.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
            else:
                data.to_csv(DATA_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')

            # 2. 演出と完了通知
            st.balloons()
            st.success("タスクが正常に保存されました")
            
            # 3. 最後に画面を切り替える
            navigate_to('main')
            st.rerun()
    
# --- 「タスク一覧」画面 ---
elif st.session_state.page == 'task_list':
    st.title("📋 タスク一覧")
    
    if st.button("🏠 ホームに戻る"):
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


    DATA_FILE = "tasks.csv"
    if os.path.isfile(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        st.dataframe(df, use_container_width=True) # 表形式で表示
    else:
        st.info("現在、登録されているタスクはありません。")

# --- 「引き継ぎ希望申請」画面 ---
elif st.session_state.page == 'application':
    st.title("🙋 引き継ぎ希望申請")
    if st.button("🏠 ホームに戻る"):
        navigate_to('main')
        st.rerun()

# --- 「結果の確認・情報リセット」画面 ---
elif st.session_state.page == 'results_reset':
    st.title("🧹 結果の確認・情報リセット")
    if st.button("🏠 ホームに戻る"):
        navigate_to('main')
        st.rerun()