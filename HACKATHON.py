import streamlit as st
import pandas as pd
import os
import itertools

#先にモデルを組む
def solve_matching(app_df, tasks_df):
    w1, w2, w3 = 0.5, 3.0, 1.0

    valid_candidates = []
    for _, row in app_df.iterrows():
        t_eval = row['タスクの内容に関する10段階評価']
        p_eval = row['引き継ぎ相手に関する10段階評価']
        s_eval = row['スケジュールに関する評価']
        
        # あなたが指定した「足切り条件」
        if t_eval <= 3 or p_eval <= 4 or s_eval <= 3:
            continue
            
        score = (t_eval * w1) + (p_eval * w2) + (s_eval * w3)
        valid_candidates.append({
            'name': row['人名'],
            'task': row['タスク名'],
            'score': score
        })
    
    all_tasks = df1['タスク名'].unique()
    all_people = df2['人名'].unique()
    
    best_total_score = -1
    best_combination = []

    for combination in itertools.permutations(all_people, len(all_tasks)):
        current_total_score = 0
        current_pairing = []
        is_valid_combo = True

        for i, task_name in enumerate(all_tasks):
            person_name = combination[i]
            # この人がそのタスクに対して有効な(足切りされていない)データを持っているか確認
            match = next((c for c in valid_candidates if c['name'] == person_name and c['task'] == task_name), None)
            
            if match:
                current_total_score += match['score']
                current_pairing.append({"タスク名": task_name, "担当者": person_name, "個人スコア": round(match['score'], 2)})
            else:
                is_valid_combo = False
                break
        
        if is_valid_combo and current_total_score > best_total_score:
            best_total_score = current_total_score
            best_combination = current_pairing
    return best_combination, best_total_score


# 1. ページの設定
st.set_page_config(
    page_title="引き継ぎ管理アプリ", 
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. デザイン（CSS）
st.markdown("""
    <style>
    .stApp { background-color: #fdfdfd; }
            
     /* メインコンテナを中央揃え */
    .main .block-container {
        max-width: 1000px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
            
    /* タイトルを中央揃え */
    h1 {
        text-align: center;
        font-size: clamp(1.5rem, 5vw, 2.5rem);
    }
    
    /* サブタイトルを中央揃え */
    .stApp > div > div > div > div > p {
        text-align: center;
    }
    
     /* ボタンのスタイル - カードっぽく */
    div.stButton > button {
        border-radius: 15px;
        border: 2px solid #6cace4;
        background-color: white;
        color: #6cace4;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
        min-height: 120px;
        margin-bottom: 15px;
        font-size: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    div.stButton > button:hover {
        background-color: #6cace4;
        color: white;
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(108, 172, 228, 0.3);
    }
            
     /* フォームのスタイル */
    .stForm {
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 20px;
        background-color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
            
     /* Dividerのスタイル */
    hr {
        margin: 2rem 0;
    }
    
    /* データフレーム・テーブルのスタイル */
    [data-testid="stDataFrame"], .stTable {
        overflow-x: auto;
    }
            
    
    /* タブレット対応（768px以上） */
    @media (min-width: 768px) {
        div.stButton > button {
            min-height: 140px;
            font-size: 20px;
        }
    }
    
    /* モバイル対応（768px以下） */
    @media (max-width: 768px) {
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        div.stButton > button {
            min-height: 100px;
            font-size: 16px;
            margin-bottom: 12px;
        }
        
        .stForm {
            padding: 15px;
        }
        
        /* 入力フィールドのフォントサイズ（iOSズーム防止） */
        input, textarea {
            font-size: 16px !important;
        }
        
        [data-testid="stDataFrame"], .stTable {
            font-size: 12px;
        }
        
        h2 {
            font-size: 1.3rem;
        }
    }
    
    /* 小型モバイル対応（480px以下） */
    @media (max-width: 480px) {
        div.stButton > button {
            min-height: 90px;
            font-size: 15px;
        }
        
        .stForm {
            padding: 10px;
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

    
 # PC: 横3列、スマホ: 縦1列に自動調整
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥\n\nタスク入力"):
            navigate_to('task_input')
            st.rerun()
    
    with col2:
        if st.button("📋\n\nタスク一覧"):
            navigate_to('task_list')
            st.rerun()
    
    with col3:
        if st.button("🙋\n\n引き継ぎ希望申請"):
            navigate_to('application')
            st.rerun()
    
    # 下段: 中央に配置
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        if st.button('🧹\n\n最適な引き継ぎ先の\n確認・情報リセット'):
            navigate_to('results_reset')
            st.rerun()


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
        df1 = pd.read_csv("tasks.csv")
        st.dataframe(df1,use_container_width=True )
        st.info(f"現在、{len(df1)}件のタスクが登録されています。")
    else:
        st.warming("まだ登録されたタスクはありません")

    
#「引き継ぎ希望申請」の画面




#『最適な引き継ぎ先の確認・情報リセット」の画面

elif st.session_state.page == 'results_reset':
    st.title("🧹 最適な引き継ぎ先の確認・情報リセット")

    if st.button("🏠 ホームに戻る"):
        navigate_to('main')
        st.rerun()

    if os.path.isfile("tasks.csv") and os.path.isfile("tasks2.csv"):
        df1 = pd.read_csv("tasks.csv")
        df2 = pd.read_csv("tasks2.csv")

        st.subheader("📊 最適な引き継ぎ先一覧")

        best_pairing, total_score = solve_matching(df2, df1)
        if best_pairing:
            st.success(f"全体の合計スコアが最大（{round(total_score, 2)}点）になる組み合わせを算出しました！")
            result_df = pd.DataFrame(best_pairing)
            st.table(result_df)
        
        else:
            st.warning("条件を満たす組み合わせが見つかりませんでした。評価を緩めるか、回答を増やしてください。")

    else:
        st.error("データが見つかりません。tasks.csv と tasks2.csv の両方が必要です。")
    
    st.divider()
    
    if st.button("🗑️ データのリセット", type="secondary"):
        if os.path.exists("tasks.csv"): 
            os.remove("tasks.csv")
        if os.path.exists("tasks2.csv"): 
            os.remove("tasks2.csv")
        st.warning("全てのデータを削除しました。")
        st.rerun()