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
    
    all_tasks = tasks_df['タスク名'].unique()
    all_people = app_df['人名'].unique()
    
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
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. デザイン（CSS）- 強制的に中央揃え
st.markdown("""
    <style>
    /* タイトル用の特別なフォントを読み込み */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Noto+Sans+JP:wght@400;500&family=Noto+Serif+JP:wght@600;700&display=swap');
    
    .stApp { 
        background: linear-gradient(180deg, #f7f9fc 0%, #ffffff 55%, #fef9ec 100%);
        font-family: 'Inter', 'Noto Sans JP', sans-serif;
        color: #0f172a;
    }
    
    /* メインコンテナを中央に */
    .main .block-container {
        max-width: 960px !important;
        padding-top: 4.5rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    
    /* タイトル専用スタイル（明朝体・セリフ体） */
    .custom-title {
        font-family: 'Noto Serif JP', serif;
        font-weight: 700;
        font-size: 2rem;
        color: #0f172a;
        text-align: center;
        margin-bottom: 1.5rem;
        letter-spacing: 0.08em;
    }

    .custom-subtitle {
        text-align: center;
        color: #334155;
        font-size: 1rem;
        margin-top: -0.5rem;
        margin-bottom: 1.5rem;
        letter-spacing: 0.02em;
    }
    
    /* 通常のタイトル（h1）：中央揃え */
    h1 {
        text-align: center;
        color: #0f172a;
        font-size: 1.9rem;
        margin-bottom: 2rem;
        font-family: 'Noto Sans JP', sans-serif;
    }

    /* Streamlitの縦方向のブロックを中央揃えに強制 */
    [data-testid="stVerticalBlock"] {
        gap: 1.2rem !important;
    }
    
    [data-testid="stVerticalBlock"] > div {
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }

    /* ボタンの親要素を中央揃えに */
    .element-container {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
    }

    /* ボタンコンテナを中央に配置 */
    div.stButton {
        width: 100% !important;
        max-width: 420px !important;
        display: flex !important;
        justify-content: center !important;
        margin: 0 auto 12px auto !important;
    }

    /* ボタン本体のベーススタイル（通常サイズ） */
    div.stButton > button {
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        background: linear-gradient(180deg, #ffffff 0%, #f7fbff 100%);
        color: #0f172a;
        width: 100% !important;
        max-width: 420px !important;
        height: 52px !important;
        min-height: 52px !important;
        margin: 0 auto !important;
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 0.01em;
        transition: all 0.2s ease;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0 18px !important;
        text-align: center;
        box-shadow: 0 8px 18px rgba(15, 23, 42, 0.08);
    }

    /* ホバー効果 */
    div.stButton > button:hover {
        border-color: #0f4c81;
        background: linear-gradient(180deg, #fdf7e3 0%, #f6fbff 100%);
        color: #0b1f3a;
        transform: translateY(-3px);
        box-shadow: 0 14px 30px rgba(15, 23, 42, 0.14);
    }

    /* ボタン内のテキスト */
    div.stButton > button > div {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
    }

    /* アイコン（絵文字）のサイズ調整 */
    div.stButton > button p {
        font-size: 1rem !important;
        margin: 0 !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
            
    /* 入力要素とフォーム */
    [data-testid="stForm"] > div {
        width: 100%;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem !important;
        box-shadow: 0 16px 40px rgba(15, 23, 42, 0.08);
    }

    /* ラベルと入力を全幅に */
    [data-testid="stForm"] label {
        width: 100% !important;
    }

    label p {
        font-weight: 600 !important;
        color: #0f172a !important;
    }

    .stTextInput, .stTextArea {
        width: 100% !important;
    }

    .stTextInput input, .stTextArea textarea {
        border-radius: 10px !important;
        border: 1px solid #cbd5e1 !important;
        padding: 0.85rem 1rem !important;
        background: #ffffff !important;
        color: #0f172a !important;
        width: 100% !important;
        min-height: 48px;
    }

    /* テキストエリアの高さを少し拡張 */
    .stTextArea textarea {
        min-height: 120px !important;
    }

    .stSlider [role="slider"] {
        background: #0f766e !important;
    }

    /* フォームの提出ボタンをやや大きく */
    [data-testid="stFormSubmitButton"] > button {
        height: 64px !important;
        min-height: 64px !important;
        max-width: 360px !important;
        font-size: 16px !important;
        padding: 0 18px !important;
        box-shadow: 0 16px 30px rgba(15, 23, 42, 0.14);
    }

    /* データフレームの余白 */
    .stDataFrame {
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.05);
    }

    /* ホームボタン用の4列レイアウト */
    .home-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 18px;
        width: 100%;
        max-width: 1050px;
        margin: 0 auto;
    }

    .home-grid .stButton button {
        height: 150px !important;
        min-height: 150px !important;
        font-size: 17px;
        box-shadow: 0 16px 36px rgba(15, 23, 42, 0.12);
    }

    /* 小さめの戻るボタン */
    .small-back button {
        height: 44px !important;
        min-height: 44px !important;
        max-width: 220px !important;
        font-size: 14px !important;
        padding: 0 16px !important;
        box-shadow: 0 6px 14px rgba(15, 23, 42, 0.08);
    }

    /* 大きめの提出ボタン */
    .large-submit button {
        height: 64px !important;
        min-height: 64px !important;
        max-width: 360px !important;
        font-size: 16px !important;
        padding: 0 18px !important;
        box-shadow: 0 16px 30px rgba(15, 23, 42, 0.14);
    }

    /* タブレット・スマホ（768px以下）向けの微調整 */
    @media (max-width: 768px) {
        .main .block-container {
            padding-top: 2.5rem;
            padding-left: 1.2rem;
            padding-right: 1.2rem;
            max-width: 100% !important;
        }
        
        .custom-title {
            font-size: 1.55rem;
        }
        
        .home-grid {
            grid-template-columns: repeat(2, 1fr);
            gap: 14px;
        }

        div.stButton > button {
            width: 100% !important;
            max-width: 100% !important;
            height: 140px !important;
            min-height: 140px !important;
            font-size: 15px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 状態管理とナビゲーション
if 'page' not in st.session_state:
    st.session_state.page = 'main'

def navigate_to(page_name):
    st.session_state.page = page_name

# ホーム画面（リスト形式）
if st.session_state.page == 'main':
    # カスタムフォントのタイトル
    st.markdown("<h1 class='custom-title'>引き継ぎ管理システム</h1>", unsafe_allow_html=True)
    st.markdown("<div class='custom-subtitle'>サークルや団体の引き継ぎをストレスフリーに</div>", unsafe_allow_html=True)
    
    # 中央揃え用のコンテナを作成
    st.markdown("<div class='home-grid'>", unsafe_allow_html=True)
    if st.button("📥 タスクを入力する", key="home_task_input"):
        navigate_to('task_input')
        st.rerun()
        
    if st.button("📋 タスク一覧を確認する", key="home_task_list"):
        navigate_to('task_list')
        st.rerun()
        
    if st.button("🙋 引き継ぎ希望を申請する", key="home_application"):
        navigate_to('application')
        st.rerun()
        
    if st.button("🧹 マッチング結果・リセット", key="home_results_reset"):
        navigate_to('results_reset')
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# 「タスク入力」画面
elif st.session_state.page == 'task_input':
    st.title("📥 タスク入力")
    
    if st.button("🏠 ホームに戻る"):
        navigate_to('main')
        st.rerun() 
    
    with st.form(key='task_form'):
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
            st.info("提出されました")
            
            # 3. 最後に画面を切り替える
            navigate_to('main')
            st.rerun()
    
# --- 「タスク一覧」画面 ---
elif st.session_state.page == 'task_list':
    st.title("📋 タスク一覧")

    if os.path.isfile("tasks.csv"):
        df1 = pd.read_csv("tasks.csv")
        st.dataframe(df1, use_container_width=True)
        st.info(f"現在、{len(df1)}件のタスクが登録されています。")
    else:
        st.warning("まだ登録されたタスクはありません")

    # 下部に戻るボタン（小さめ）
    col_back = st.columns([1,1,1,1,1])
    with col_back[2]:
        if st.button("🏠 ホームに戻る", key="task_list_back", help="ホームへ戻る"):
            navigate_to('main')
            st.rerun()

# 「引き継ぎ希望申請」画面
elif st.session_state.page == 'application':
    st.title("🙋 引き継ぎ希望申請")
    
    # 登録タスクの表示
    if os.path.isfile("tasks.csv"):
        df = pd.read_csv("tasks.csv")
        
        st.subheader("📋 対象タスク情報")
        st.write("**タスク名:** " + str(df.loc[0, "タスク名"])) 
        st.write("**タスクの詳細:** " + str(df.loc[0, "タスクの詳細"]))
        st.write("**タスクを行う時期・日時:** " + str(df.loc[0, "タスクを行う時期・日時"]))
        st.write("**引き継ぎ担当者:** " + str(df.loc[0, "引き継ぎ担当者"]))
        
        st.divider()

        with st.form(key='evaluate_form', clear_on_submit=False):
            st.subheader("📊 評価入力")
            
            # スライダーで10段階評価する
            contentValue = st.slider(
                'タスクの内容に関する評価', 0, 10, key='content'
            )
            personValue = st.slider(
                '引継ぎ相手に関する評価', 0, 10, key='person'
            )
            scheduleValue = st.slider(
                'スケジュールに関する評価', 0, 10, key='schedule'
            )

            # 提出ボタン
            submitted = st.form_submit_button("提出", help="評価を送信", on_click=None, use_container_width=True, type="primary")

            # 保存処理
            if submitted:
                if contentValue * personValue * scheduleValue != 0:
                    # csvにデータを書き込み
                    DATA_FILE2 = "tasks2.csv"

                    # 評価データ
                    if os.path.isfile("tasks2.csv"):
                        personIndex = len(pd.read_csv("tasks2.csv")) + 1
                    else:
                        personIndex = 1
                    
                    data2 = pd.DataFrame(
                        [["匿名" + str(personIndex), df.loc[0, "タスク名"], contentValue, personValue, scheduleValue]], 
                        columns=["人名", "タスク名", "タスクの内容に関する10段階評価", "引き継ぎ相手に関する10段階評価", "スケジュールに関する評価"]
                    )  

                    if not os.path.isfile(DATA_FILE2):
                        data2.to_csv(DATA_FILE2, index=False, encoding='utf-8-sig')
                    else:
                        data2.to_csv(DATA_FILE2, mode='a', header=False, index=False, encoding='utf-8-sig')
                
                    # 成功表示
                    st.success("評価が完了しました。")
                    st.balloons()
                    
                    # ホームに戻る
                    navigate_to('main')
                    st.rerun()
                    
                # 評価していない項目があれば警告
                else:
                    st.error("全評価を1~10段階で行ってください。")

        # 下部に戻るボタン（小さめ）
        col_back2 = st.columns([1,1,1,1,1])
        with col_back2[2]:
            if st.button("🏠 ホームに戻る", key="application_back", help="ホームへ戻る"):
                navigate_to('main')
                st.rerun()
    else:
        st.warning("まだ登録されたタスクがありません。先にタスクを登録してください。")

# --- 「最適な引き継ぎ先の確認・情報リセット」画面 ---
elif st.session_state.page == 'results_reset':
    st.title("🧹 最適な引き継ぎ先の確認・情報リセット")

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
    
    col_reset, col_back, col_empty = st.columns([1,1,1])
    with col_reset:
        if st.button("🗑️ データのリセット", type="secondary"):
            if os.path.exists("tasks.csv"): 
                os.remove("tasks.csv")
            if os.path.exists("tasks2.csv"): 
                os.remove("tasks2.csv")
            st.warning("全てのデータを削除しました。")
            st.rerun()
    with col_back:
        if st.button("🏠 ホームに戻る", key="results_back", help="ホームへ戻る"):
            navigate_to('main')
            st.rerun()
